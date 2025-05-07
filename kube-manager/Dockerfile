# Build stage
FROM golang:1.20 as builder

WORKDIR /app

# Copy and download Go modules
COPY go.mod ./
RUN go mod download

# Copy the entire source code
COPY . .

# Build the binary for Linux
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o app .

# Final image
FROM alpine:latest

# Install necessary certificates
RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Copy the binary from the builder stage
COPY --from=builder /app/app .

# Expose the application port
EXPOSE 8080

# Startup command
ENTRYPOINT ["./app"]
