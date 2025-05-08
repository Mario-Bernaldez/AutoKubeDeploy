# Generator Engine

HTTP service for automatically generating Kubernetes YAML manifests from structured JSON. Ideal for integration into DevOps tools, graphical interfaces, or automated workflows.

## Features

- Supports multiple Kubernetes resource types:
  - Namespace
  - Deployment
  - Service
  - HorizontalPodAutoscaler (HPA)
  - ConfigMap
  - Secret (Opaque, TLS, Docker config)
  - PersistentVolumeClaim (PVC)
  - Ingress
  - ServiceAccount
  - Role / ClusterRole with Binding
  - NetworkPolicy
- Output in valid `YAML` format, ready to apply using `kubectl`.
- Simple REST API for integration over HTTP.

## Available Endpoint

```
POST /generate
```

Sends a JSON payload corresponding to one of the supported types. The service responds with the generated YAML as plain text.