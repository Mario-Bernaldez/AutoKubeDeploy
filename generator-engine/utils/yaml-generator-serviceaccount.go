package utils

import (
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GenerateServiceAccountYAML(sa models.ServiceAccountObject) (string, error) {
	imagePullSecrets := make([]map[string]string, 0)
	for _, name := range sa.ImagePullSecrets {
		imagePullSecrets = append(imagePullSecrets, map[string]string{
			"name": name,
		})
	}

	serviceAccountYAML := map[string]interface{}{
		"apiVersion": "v1",
		"kind":       "ServiceAccount",
		"metadata": map[string]interface{}{
			"name":      sa.ServiceAccountName,
			"namespace": sa.Namespace,
		},
		"imagePullSecrets": imagePullSecrets,
	}

	out, err := yaml.Marshal(serviceAccountYAML)
	if err != nil {
		return "", err
	}
	return string(out), nil
}
