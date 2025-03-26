package models

type RequestPayload struct {
	YAML   string `json:"yaml"`
	Model  string `json:"model"`
}

type ResponsePayload struct {
	Explanation string `json:"explanation"`
}

type OpenAIMessage struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type OpenAIRequest struct {
	Model    string          `json:"model"`
	Messages []OpenAIMessage `json:"messages"`
}

type OpenAIResponse struct {
	Choices []struct {
		Message OpenAIMessage `json:"message"`
	} `json:"choices"`
}
