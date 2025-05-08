# YAML Explainer

HTTP microservice that receives a Kubernetes YAML manifest and returns a human-readable explanation using a selected AI model (via OpenRouter API).

## Features

- Accepts any Kubernetes YAML manifest as input
- Validates input for YAML syntax
- Uses OpenRouter-compatible AI models to provide natural language explanations
- Allows model selection
- Includes endpoint to fetch available models (with optional filter for free ones)

## Available Endpoints

### POST `/explain`

Submits a YAML manifest to be explained by an AI model.

- **Headers**:  
  `Content-Type: application/json`

- **Body**:
  ```json
  {
    "yaml": "<kubernetes_manifest_as_string>",
    "model": "openchat/openchat-7b:free"
  }
  ```

- **Response**:
  ```json
  {
    "explanation": "This manifest creates a Kubernetes Deployment named 'nginx'..."
  }
  ```

- **Example with curl**:
  ```bash
  curl -X POST http://localhost:8080/explain        -H "Content-Type: application/json"        -d '{"yaml": "apiVersion: v1\nkind: Pod\n...", "model": "openchat/openchat-7b:free"}'
  ```

---

### GET `/models`

Returns a list of available models from OpenRouter.

- **Optional query param**: `?free=true` to filter only free-tier models.

- **Response**:
  ```json
  [
    { "id": "openchat/openchat-7b:free", "name": "OpenChat 7B", "free": true },
    { "id": "another-model", "name": "Another Model", "free": false }
  ]
  ```

---

## Requirements

- Environment variable `OPENROUTER_API_KEY` must be defined.
- Internet access to call `https://openrouter.ai/api/v1`.

---

## Running Locally

1. Set your API key:
   ```bash
   export OPENROUTER_API_KEY=your-api-key-here
   ```

2. Run the server:
   ```bash
   go run main.go
   ```

The server will be available at `http://localhost:8080`.

---

## Project Structure

```
yaml-explainer/
├── handlers/       # HTTP endpoint handlers
├── models/         # Request/response and OpenAI structures
├── openai/         # External API logic
├── utils/          # YAML validation helpers
├── main.go         # Entry point
```
