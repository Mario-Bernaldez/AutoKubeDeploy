package handlers

import (
	"encoding/json"
	"net/http"
	"strings"
	"yaml-explainer/openai"
)

func GetAvailableModels(w http.ResponseWriter, r *http.Request) {
	models, err := openai.FetchSimplifiedModels()
	if err != nil {
		http.Error(w, "Error fetching models: "+err.Error(), http.StatusInternalServerError)
		return
	}

	query := r.URL.Query()
	if strings.ToLower(query.Get("free")) == "true" {
		var filtered []openai.SimplifiedModel
		for _, m := range models {
			if m.Free {
				filtered = append(filtered, m)
			}
		}
		models = filtered
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(models)
}
