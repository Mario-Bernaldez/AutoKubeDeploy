package handlers

import (
	"encoding/json"
	"log"
	"net/http"
	"yaml-explainer/models"
	"yaml-explainer/openai"
	"yaml-explainer/utils"
)

func ExplainHandler(w http.ResponseWriter, r *http.Request) {
	log.Println("New request received at /explain")

	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var payload models.RequestPayload
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		http.Error(w, "Error reading request body", http.StatusBadRequest)
		return
	}

	if !utils.IsValidYAML(payload.YAML) {
		http.Error(w, "Invalid YAML", http.StatusBadRequest)
		return
	}

	response, statusCode, err := openai.ExplainYAMLWithModel(payload.YAML, payload.Model)
	if err != nil {
		log.Printf("Error (%d): %v\n", statusCode, err)
		http.Error(w, err.Error(), statusCode)
		return
	}

	json.NewEncoder(w).Encode(models.ResponsePayload{
		Explanation: response,
	})
}
