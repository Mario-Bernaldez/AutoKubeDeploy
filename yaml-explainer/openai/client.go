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
const model = "open-r1/olympiccoder-7b:free" // Puedes cambiar por otro gratuito

func ExplainYAML(yaml string) (string, error) {
	payload := models.OpenAIRequest{
		Model: model,
		Messages: []models.OpenAIMessage{
			{Role: "system", Content: "Eres un experto en DevOps. Explica detalladamente qué hace este manifiesto YAML de Kubernetes."},
			{Role: "user", Content: yaml},
		},
	}

	body, _ := json.Marshal(payload)

	apiKey := os.Getenv("OPENROUTER_API_KEY")
	if apiKey == "" {
		return "", errors.New("la variable de entorno OPENROUTER_API_KEY no está definida")
	}

	req, err := http.NewRequest("POST", endpoint, bytes.NewBuffer(body))
	if err != nil {
		return "", err
	}

	req.Header.Set("Authorization", "Bearer "+apiKey)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("HTTP-Referer", "https://tu-proyecto.com") // usa un dominio propio o válido
	req.Header.Set("X-Title", "yaml-explainer")

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	respBody, _ := io.ReadAll(resp.Body)

	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("OpenRouter error %d: %s", resp.StatusCode, string(respBody))
	}

	var result models.OpenAIResponse
	if err := json.Unmarshal(respBody, &result); err != nil {
		return "", fmt.Errorf("error al parsear respuesta JSON: %v\nContenido: %s", err, string(respBody))
	}

	if len(result.Choices) == 0 {
		return "", fmt.Errorf("respuesta vacía de OpenRouter:\n%s", string(respBody))
	}

	return result.Choices[0].Message.Content, nil
}
