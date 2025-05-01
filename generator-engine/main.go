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

	log.Println("Servidor iniciado en el puerto 8080")
	log.Fatal(http.ListenAndServe(":8080", r))
}
