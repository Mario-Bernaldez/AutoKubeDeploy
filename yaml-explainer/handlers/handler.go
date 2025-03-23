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
	log.Println("Nueva petición recibida en /explain")

	if r.Method != http.MethodPost {
		http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
		return
	}

	var payload models.RequestPayload
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		http.Error(w, "Error leyendo el cuerpo", http.StatusBadRequest)
		return
	}

	if !utils.IsValidYAML(payload.YAML) {
		http.Error(w, "YAML inválido", http.StatusBadRequest)
		return
	}

	response, err := openai.ExplainYAML(payload.YAML)
	if err != nil {
		http.Error(w, "Error en OpenAI: "+err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(models.ResponsePayload{
		Explanation: response,
	})
}
