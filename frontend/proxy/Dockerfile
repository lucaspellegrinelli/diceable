# Use the official Golang image to build the application
FROM golang:1.19 AS build

# Set the working directory
WORKDIR /app

# Copy the go.mod and go.sum files
COPY go.mod go.sum ./

# Download and cache dependencies
RUN go mod download

# Copy the source code
COPY . .

# Build the application
RUN go build -o websocket-proxy .

# Use a minimal base image to run the application
FROM alpine:latest

# Set environment variables
ENV SUBURB_HOST=""
ENV SUBURB_TOKEN=""

# Install necessary packages
RUN apk --no-cache add ca-certificates

# Copy the built application from the previous stage
COPY --from=build /app/websocket-proxy /usr/local/bin/websocket-proxy

# Expose the port the application will run on
EXPOSE 3000

# Run the application
CMD ["websocket-proxy"]
