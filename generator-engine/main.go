package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"generator-engine/handlers"
)

func main() {
	r := mux.NewRouter()
	r.HandleFunc("/generate", handlers.GenerateHandler).Methods("POST")

	log.Println("Servidor iniciado en el puerto 8080")
	log.Fatal(http.ListenAndServe(":8080", r))
}
