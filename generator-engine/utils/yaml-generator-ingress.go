package utils

import (
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GenerateIngressYAML(ing models.IngressObject) (string, error) {
	paths := make([]map[string]interface{}, 0)
	for _, p := range ing.Paths {
		paths = append(paths, map[string]interface{}{
			"path":     p.Path,
			"pathType": "Prefix", // puedes parametrizarlo si quieres
			"backend": map[string]interface{}{
				"service": map[string]interface{}{
					"name": p.ServiceName,
					"port": map[string]interface{}{
						"number": p.ServicePort,
					},
				},
			},
		})
	}

	ingressYAML := map[string]interface{}{
		"apiVersion": "networking.k8s.io/v1",
		"kind":       "Ingress",
		"metadata": map[string]interface{}{
			"name":      ing.IngressName,
			"namespace": ing.Namespace,
		},
		"spec": map[string]interface{}{
			"rules": []map[string]interface{}{
				{
					"host": ing.Host,
					"http": map[string]interface{}{
						"paths": paths,
					},
				},
			},
		},
	}

	out, err := yaml.Marshal(ingressYAML)
	if err != nil {
		return "", err
	}
	return string(out), nil
}
