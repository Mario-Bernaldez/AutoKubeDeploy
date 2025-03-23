# Etapa 1: Construcción del binario en una imagen intermedia
FROM golang:1.24.1 AS builder

WORKDIR /app

# Copiar los archivos del módulo
COPY go.mod go.sum ./
RUN go mod download

# Copiar el resto del código fuente
COPY . .

# Compilar el binario
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o generator-engine main.go

# Etapa 2: Imagen final con el binario compilado
FROM alpine:latest

WORKDIR /root/

# Instalar dependencias necesarias
RUN apk --no-cache add ca-certificates

# Copiar el binario desde la imagen builder
COPY --from=builder /app/generator-engine .

# Exponer el puerto de la aplicación
EXPOSE 8080

# Comando de inicio
CMD ["./generator-engine"]
