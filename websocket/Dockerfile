FROM golang:1.22-alpine AS build

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o websocket .

FROM gcr.io/distroless/static-debian12

ENV PORT="5555"
ENV ORIGIN_SOURCE=""

COPY --from=build /app/websocket /usr/local/bin/websocket

EXPOSE 5555

ENTRYPOINT ["/usr/local/bin/websocket"]
