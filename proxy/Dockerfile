# Use the official Rust image as the base
FROM rust:latest AS builder

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the Cargo.toml and Cargo.lock files
COPY Cargo.toml Cargo.lock ./

# Copy the source code
COPY src ./src

# Build the project
RUN cargo build --release

# Use a minimal image to run the application
FROM debian:buster-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the built binary from the builder stage
COPY --from=builder /usr/src/app/target/release/websocket_proxy .

# Expose the port that the application will run on
EXPOSE $PORT

# Set environment variables
ENV SUBURB_HOST $SUBURB_HOST
ENV SUBURB_TOKEN $SUBURB_TOKEN
ENV ORIGIN_SOURCE $ORIGIN_SOURCE
ENV PORT $PORT

# Run the application
CMD ["./websocket_proxy"]
