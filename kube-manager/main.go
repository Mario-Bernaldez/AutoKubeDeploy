package main

import (
    "fmt"
    "log"
    "net/http"

    "kube-manager/handlers"
)

func main() {
    http.HandleFunc("/deploy", handlers.DeployHandler)
    http.HandleFunc("/list", handlers.ListHandler)

    fmt.Println("Escuchando en :8080...")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
