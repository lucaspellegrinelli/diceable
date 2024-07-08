# Use official Rust image as the build environment
FROM rust:latest AS build

# Create a new directory for the application
WORKDIR /usr/src/app

# Copy the project files
COPY . .

# Build the project
RUN cargo build --release

# Use a minimal base image for the final image
FROM debian:buster-slim

# Copy the built binary from the build stage
COPY --from=build /usr/src/app/target/release/websocket_proxy /usr/local/bin/websocket_proxy

# Set the startup command
CMD ["websocket_proxy"]

# Expose the port
EXPOSE 3030
