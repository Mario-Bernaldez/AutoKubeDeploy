package openai

import (
	"bytes"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"yaml-explainer/models"
)

func ExplainKubernetesError(errMsg string, model string) (string, int, error) {
	if model == "" {
		model = "openchat/openchat-7b:free"
	}

	payload := models.OpenAIRequest{
		Model: model,
		Messages: []models.OpenAIMessage{
			{
				Role:    "system",
				Content: "Eres un experto en DevOps y Kubernetes. Explica de forma clara y directa qué significa este error generado al aplicar un manifiesto YAML de Kubernetes, y si es posible sugiere una solución. No uses listas, markdown, ni estilos especiales. Solo una explicación concisa y neutral.",
			},
			{Role: "user", Content: errMsg},
		},
	}

	body, _ := json.Marshal(payload)

	apiKey := os.Getenv("OPENROUTER_API_KEY")
	if apiKey == "" {
		return "", http.StatusInternalServerError, errors.New("OPENROUTER_API_KEY not set")
	}

	req, err := http.NewRequest("POST", endpoint, bytes.NewBuffer(body))
	if err != nil {
		return "", http.StatusInternalServerError, err
	}

	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("HTTP-Referer", "https://your-project.com")
	req.Header.Set("X-Title", "yaml-explainer")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", http.StatusBadGateway, err
	}
	defer resp.Body.Close()

	respBody, _ := io.ReadAll(resp.Body)

	if resp.StatusCode != http.StatusOK {
		return "", resp.StatusCode, fmt.Errorf("OpenRouter error %d: %s", resp.StatusCode, string(respBody))
	}

	var result models.OpenAIResponse
	if err := json.Unmarshal(respBody, &result); err != nil {
		return "", http.StatusInternalServerError, fmt.Errorf("error parsing JSON response: %v\nContent: %s", err, string(respBody))
	}

	if len(result.Choices) == 0 {
		return "", http.StatusInternalServerError, fmt.Errorf("empty response from OpenRouter:\n%s", string(respBody))
	}

	return result.Choices[0].Message.Content, http.StatusOK, nil
}
