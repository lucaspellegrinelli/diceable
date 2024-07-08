FROM golang:1.21 AS build

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN GOOS=linux GOARCH=amd64 go build -o proxy .

FROM alpine:latest

ENV SUBURB_HOST=""
ENV SUBURB_TOKEN=""
ENV ORIGIN_SOURCE=""

RUN apk --no-cache add ca-certificates libc6-compat

COPY --from=build /app/proxy /usr/local/bin/proxy

RUN chmod +x /usr/local/bin/proxy

EXPOSE 3000

CMD ["proxy"]
