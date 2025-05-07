package openai

import (
	"encoding/json"
	"errors"
	"net/http"
	"os"
	"strings"
)

const modelsEndpoint = "https://openrouter.ai/api/v1/models"

type RawModel struct {
	ID    string   `json:"id"`
	Name  string   `json:"name,omitempty"`
	Tiers []string `json:"tiers,omitempty"` // some models may include this
}

type SimplifiedModel struct {
	ID   string `json:"id"`
	Name string `json:"name"`
	Free bool   `json:"free"`
}

func FetchSimplifiedModels() ([]SimplifiedModel, error) {
	apiKey := os.Getenv("OPENROUTER_API_KEY")
	if apiKey == "" {
		return nil, errors.New("OPENROUTER_API_KEY not set")
	}

	req, err := http.NewRequest("GET", modelsEndpoint, nil)
	if err != nil {
		return nil, err
	}

	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("HTTP-Referer", "https://your-app.com")
	req.Header.Set("X-Title", "yaml-explainer")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var response struct {
		Data []RawModel `json:"data"`
	}
	if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
		return nil, err
	}

	// Transform into our simplified structure
	var result []SimplifiedModel
	for _, m := range response.Data {
		model := SimplifiedModel{
			ID:   m.ID,
			Name: m.Name,
			Free: strings.HasSuffix(m.ID, ":free"),
		}
		result = append(result, model)
	}

	return result, nil
}
