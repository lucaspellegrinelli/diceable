use std::convert::Infallible;
use std::env;
use warp::Filter;
use tokio_tungstenite::tungstenite::protocol::Message;
use tokio_tungstenite::connect_async;
use futures::StreamExt;

#[tokio::main]
async fn main() {
    // Load environment variables
    dotenv::dotenv().ok();
    let suburb_host = env::var("SUBURB_HOST").expect("SUBURB_HOST must be set");
    let suburb_token = env::var("SUBURB_TOKEN").expect("SUBURB_TOKEN must be set");

    // Define the WebSocket route
    let suburb_host = warp::any().map(move || suburb_host.clone());
    let suburb_token = warp::any().map(move || suburb_token.clone());
    let ws_route = warp::path!("rolls" / String)
        .and(warp::ws())
        .and(suburb_host)
        .and(suburb_token)
        .map(|id: String, ws: warp::ws::Ws, suburb_host: String, suburb_token: String| {
            ws.on_upgrade(move |websocket| handle_ws(id, websocket, suburb_host, suburb_token))
        });

    // Start the Warp server
    warp::serve(ws_route).run(([0, 0, 0, 0], 3000)).await;
}

async fn handle_ws(id: String, websocket: warp::ws::WebSocket, suburb_host: String, suburb_token: String) {
    let target_url = format!("wss://{}/pubsub/{}/listen", suburb_host, id);
    let request = http::Request::builder()
        .uri(target_url)
        .header("Authorization", suburb_token)
        .body(())
        .unwrap();

    let (target_ws_stream, _) = connect_async(request).await.expect("Failed to connect to target WebSocket");
    let (mut client_ws_sender, mut client_ws_receiver) = websocket.split();
    let (mut target_ws_sender, mut target_ws_receiver) = target_ws_stream.split();

    let client_to_target = async {
        while let Some(result) = client_ws_receiver.next().await {
            match result {
                Ok(msg) => {
                    if target_ws_sender.send(msg).await.is_err() {
                        break;
                    }
                }
                Err(_) => break,
            }
        }
    };

    let target_to_client = async {
        while let Some(result) = target_ws_receiver.next().await {
            match result {
                Ok(msg) => {
                    if client_ws_sender.send(msg).await.is_err() {
                        break;
                    }
                }
                Err(_) => break,
            }
        }
    };

    tokio::join!(client_to_target, target_to_client);
}
