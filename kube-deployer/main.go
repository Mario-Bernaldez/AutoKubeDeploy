package main

import (
    "fmt"
    "log"
    "net/http"

    "kube-deployer/handlers"
)

func main() {
    http.HandleFunc("/deploy", handlers.DeployHandler)

    fmt.Println("Escuchando en :8080...")
    log.Fatal(http.ListenAndServe(":8080", nil))
}
