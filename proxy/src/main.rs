use actix_web::{web, App, HttpServer, HttpRequest, HttpResponse, Error};
use actix_web::http::header;
use actix_web::middleware::cors::Cors;
use actix_web_actors::ws;
use reqwest::Client;
use std::env;

struct MyWs;

impl actix::Actor for MyWs {
    type Context = ws::WebsocketContext<Self>;
}

impl actix::StreamHandler<Result<ws::Message, ws::ProtocolError>> for MyWs {
    fn handle(&mut self, msg: Result<ws::Message, ws::ProtocolError>, ctx: &mut Self::Context) {
        match msg {
            Ok(ws::Message::Text(text)) => ctx.text(text),
            Ok(ws::Message::Binary(bin)) => ctx.binary(bin),
            _ => (),
        }
    }
}

async fn ws_index(
    req: HttpRequest,
    stream: web::Payload,
    client: web::Data<Client>,
) -> Result<HttpResponse, Error> {
    let id = req.match_info().get("id").unwrap_or("");
    let url = format!("{}/pubsub/{}/listen", env::var("SUBURB_HOST").unwrap(), id);

    let mut request = client.get(&url)
        .header("Authorization", format!("wss://{}", env::var("SUBURB_TOKEN").unwrap()))
        .build()
        .unwrap();

    let res = client.execute(request).await.unwrap();
    if res.status().is_success() {
        ws::start(MyWs {}, &req, stream)
    } else {
        Ok(HttpResponse::InternalServerError().finish())
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenv::dotenv().ok();
    let client = Client::new();
    let origin_source = env::var("ORIGIN_SOURCE").unwrap();
    let port = env::var("PORT").unwrap_or_else(|_| "8080".to_string());

    HttpServer::new(move || {
        let cors = Cors::default()
            .allowed_origin(&origin_source)
            .allowed_methods(vec!["GET"])
            .allowed_headers(vec![header::AUTHORIZATION, header::CONTENT_TYPE])
            .supports_credentials();

        App::new()
            .wrap(cors)
            .app_data(web::Data::new(client.clone()))
            .route("/rolls/{id}", web::get().to(ws_index))
    })
    .bind(format!("0.0.0.0:{}", port))?
    .run()
    .await
}
