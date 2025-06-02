package main

import (
	"fmt"
	"log"
	"net/http"

	"yaml-explainer/handlers"
)

func main() {
	http.HandleFunc("/explain", handlers.ExplainHandler)
	fmt.Println("✅ Microservicio escuchando en http://localhost:8080")
	http.HandleFunc("/models", handlers.GetAvailableModels)
	http.HandleFunc("/explain-error", handlers.ExplainErrorHandler)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
