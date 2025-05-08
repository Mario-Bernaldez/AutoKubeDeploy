# Kubernetes YAML Configurator (Django Web App)

A Django-based web application that provides a user interface to configure, generate, explain, and apply Kubernetes resource manifests (YAML). It integrates with three backend services:

- **generator-engine**: Generates Kubernetes YAML based on structured input.
- **yaml-explainer**: Uses AI models to explain YAML manifests.
- **kube-manager**: Applies, lists, and deletes Kubernetes resources.

## Features

- Web UI for configuring:
  - Deployments, Services, Namespaces, HPAs, ConfigMaps, Secrets, PVCs, Ingresses, ServiceAccounts, RBAC, and Network Policies
- Sends configurations to `generator-engine` to generate YAML
- Uses `yaml-explainer` to describe generated YAML via OpenRouter-compatible models
- Applies manifests to a Kubernetes cluster using `kube-manager`
- Resource exploration and deletion
- Deployment history tracking

## Usage

1. **Navigate to the object selector**
   Choose the type of Kubernetes object you want to create.

2. **Fill the form**
   Based on the selected object, a dynamic form is shown. Complete it with your configuration.

3. **Generate YAML**
   The data is sent to `generator-engine`, and the YAML is rendered.

4. **Explain YAML**
   Select an AI model to explain what the YAML does using `yaml-explainer`.

5. **Apply to cluster**
   Apply the manifest directly to the Kubernetes cluster via `kube-manager`.

6. **View deployment history**
   Previous deployments are stored and viewable.

## Requirements

- Python 3.8+
- Django 4.x
- Kubernetes cluster with in-cluster services:
  - `generator-engine`
  - `yaml-explainer`
  - `kube-manager`
- Environment variable `OPENROUTER_API_KEY` set in `yaml-explainer`

## 🛠️ Running Locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run Django server:

   ```bash
   python manage.py runserver
   ```

3. Access the app at `http://localhost:8000/`

## Project Structure

```
kube-configurator/
├── templates/                 # HTML templates
├── forms.py                  # Django forms for each resource type
├── models.py                 # DeploymentHistory model
├── views.py                  # Main logic for form handling and YAML generation
├── urls.py                   # URL routes
├── static/                   # Optional static files
├── requirements.txt          # Python dependencies
```

## Integration Endpoints

- `http://generator-engine/generate` – Generates YAML
- `http://yaml-explainer:8080/explain` – Explains YAML
- `http://yaml-explainer:8080/models` – Lists AI models
- `http://kube-manager:8080/deploy` – Applies YAML
- `http://kube-manager:8080/list` – Lists resources
- `http://kube-manager:8080/resource` – Deletes resources
