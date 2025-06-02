package handlers

import (
	"encoding/json"
	"log"
	"net/http"
	"yaml-explainer/models"
	"yaml-explainer/openai"
)

func ExplainErrorHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("New request received at /explain-error")

	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var payload models.ErrorRequestPayload
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		http.Error(w, "Invalid JSON body", http.StatusBadRequest)
		return
	}

	response, statusCode, err := openai.ExplainKubernetesError(payload.ErrorMessage, payload.Model)
	if err != nil {
		log.Printf("Error (%d): %v\n", statusCode, err)
		http.Error(w, err.Error(), statusCode)
		return
	}

	json.NewEncoder(w).Encode(models.ResponsePayload{
		Explanation: response,
	})
}
