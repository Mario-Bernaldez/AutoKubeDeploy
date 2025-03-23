# Etapa 1: Construcción del binario en una imagen intermedia
FROM golang:1.24.1 AS builder

WORKDIR /app

# Copiar los archivos del módulo
COPY go.mod go.sum ./
RUN go mod download

# Copiar el resto del código fuente
COPY . .

# Compilar el binario estático
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o yaml-explainer main.go

# Etapa 2: Imagen final con el binario compilado
FROM alpine:latest

WORKDIR /root/

# Instalar certificados SSL necesarios para hacer peticiones HTTPS
RUN apk --no-cache add ca-certificates

# Copiar el binario desde la imagen builder
COPY --from=builder /app/yaml-explainer .

# Exponer el puerto de la aplicación
EXPOSE 8080

# Comando de inicio
CMD ["./yaml-explainer"]
