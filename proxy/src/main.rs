use warp::Filter;
use warp::http::header::{HeaderValue, AUTHORIZATION};
use tokio_tungstenite::tungstenite::protocol::Message;
use futures_util::{SinkExt, StreamExt};
use hyper::Uri;
use hyper::client::HttpConnector;
use hyper_tls::HttpsConnector;
use std::env;

#[tokio::main]
async fn main() {
    // Read environment variables
    let port: u16 = env::var("PORT").unwrap_or_else(|_| "3030".to_string()).parse().unwrap();
    let origin_source = env::var("ORIGIN_SOURCE").unwrap();
    let suburb_host = env::var("SUBURB_HOST").unwrap();
    let suburb_token = env::var("SUBURB_TOKEN").unwrap();

    // CORS configuration
    let cors = warp::cors()
        .allow_origin(origin_source)
        .allow_headers(vec!["content-type"])
        .allow_methods(vec!["GET", "POST"]);

    // WebSocket proxy route
    let ws_route = warp::path!("rolls" / String)
        .and(warp::ws())
        .and_then(move |id: String, ws: warp::ws::Ws| {
            let suburb_host = suburb_host.clone();
            let suburb_token = suburb_token.clone();

            async move {
                Ok(ws.on_upgrade(move |websocket| {
                    handle_websocket(websocket, id, suburb_host, suburb_token)
                }))
            }
        });

    // Start the server
    warp::serve(ws_route.with(cors))
        .run(([0, 0, 0, 0], port))
        .await;
}

async fn handle_websocket(websocket: warp::ws::WebSocket, id: String, suburb_host: String, suburb_token: String) {
    let uri = format!("{}/pubsub/{}/listen", suburb_host, id);
    let url = Uri::try_from(uri).unwrap();

    let (mut ws_tx, mut ws_rx) = websocket.split();

    // Create an HTTP client with TLS support
    let https = HttpsConnector::new();
    let client = hyper::Client::builder().build::<_, hyper::Body>(https);

    // Connect to the suburb pubsub endpoint
    let (mut suburb_ws_tx, suburb_ws_rx) = tokio_tungstenite::connect_async(url).await.unwrap().0.split();

    // Add authentication header
    let request = hyper::Request::builder()
        .header(AUTHORIZATION, HeaderValue::from_str(&suburb_token).unwrap())
        .uri(uri)
        .body(hyper::Body::empty())
        .unwrap();

    client.request(request).await.unwrap();

    // Proxy messages from client to suburb
    tokio::spawn(async move {
        while let Some(Ok(message)) = ws_rx.next().await {
            if suburb_ws_tx.send(message).await.is_err() {
                break;
            }
        }
    });

    // Proxy messages from suburb to client
    tokio::spawn(async move {
        while let Some(Ok(message)) = suburb_ws_rx.next().await {
            if ws_tx.send(message).await.is_err() {
                break;
            }
        }
    });
}
