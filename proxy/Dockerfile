# Use the official Rust image to build the application
FROM rust:1.64 AS build

# Set the working directory
WORKDIR /app

# Copy the source code
COPY . .

# Build the application
RUN cargo build --release

# Use a minimal base image to run the application
FROM debian:buster-slim

# Set environment variables
ENV SUBURB_HOST=""
ENV SUBURB_TOKEN=""

# Install necessary packages
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

# Copy the built application from the previous stage
COPY --from=build /app/target/release/websocket-proxy /usr/local/bin/websocket-proxy

# Expose the port the application will run on
EXPOSE 3000

# Run the application
CMD ["websocket-proxy"]
