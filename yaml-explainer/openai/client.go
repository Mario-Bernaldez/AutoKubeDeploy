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

const endpoint = "https://openrouter.ai/api/v1/chat/completions"
const model = "open-r1/olympiccoder-7b:free" // You can replace this with another free one

func ExplainYAMLWithModel(yaml string, model string) (string, int, error) {
	if model == "" {
		model = "openchat/openchat-7b:free"
	}

	payload := models.OpenAIRequest{
		Model: model,
		Messages: []models.OpenAIMessage{
			{
				Role:    "system",
				Content: "Eres un experto en DevOps. Explica directamente y con precisión qué hace este manifiesto YAML de Kubernetes, sin introducir, resumir ni aplicar estilo. No utilices formatos especiales como listas, markdown, emojis ni encabezados. Tu salida debe ser exclusivamente una explicación directa y neutral.",
			},
			{Role: "user", Content: yaml},
		},
	}

	body, _ := json.Marshal(payload)

	apiKey := os.Getenv("OPENROUTER_API_KEY")
	if apiKey == "" {
		return "", http.StatusInternalServerError, errors.New("environment variable OPENROUTER_API_KEY is not defined")
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

	var maybeError map[string]interface{}
	if err := json.Unmarshal(respBody, &maybeError); err == nil {
		if errField, ok := maybeError["error"].(map[string]interface{}); ok {
			if codeFloat, ok := errField["code"].(float64); ok {
				code := int(codeFloat)
				return "", code, fmt.Errorf("OpenRouter error %d: %s", code, respBody)
			}
		}
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
