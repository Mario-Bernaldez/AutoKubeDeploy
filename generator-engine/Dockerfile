# Stage 1: Build the binary in an intermediate image
FROM golang:1.24.1 AS builder

WORKDIR /app

# Copy module files
COPY go.mod go.sum ./
RUN go mod download

# Copy the rest of the source code
COPY . .

# Build the binary
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o generator-engine main.go

# Stage 2: Final image with the compiled binary
FROM alpine:latest

WORKDIR /root/

# Install necessary dependencies
RUN apk --no-cache add ca-certificates

# Copy the binary from the builder image
COPY --from=builder /app/generator-engine .

# Expose the application port
EXPOSE 8080

# Startup command
CMD ["./generator-engine"]
