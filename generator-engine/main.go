package main

import (
	"log"
	"net/http"

	"generator-engine/handlers"
	"github.com/gorilla/mux"
)

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/generate", handlers.GenerateHandler).Methods("POST")

	log.Println("Server started on port 8080")
	log.Fatal(http.ListenAndServe(":8080", r))
}
