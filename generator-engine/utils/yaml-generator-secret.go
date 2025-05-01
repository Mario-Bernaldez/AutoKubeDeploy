package utils

import (
	"encoding/base64"
	"errors"
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GenerateSecretYAML(secret models.SecretObject) (string, error) {
	encodedData := make(map[string]string)

	switch secret.SecretType {
	case "Opaque":
		keys, ok := secret.Data.([]interface{})
		if !ok {
			return "", errors.New("datos inválidos para Secret Opaque")
		}
		for _, item := range keys {
			entry, ok := item.(map[string]interface{})
			if ok {
				key := entry["key_name"].(string)
				value := entry["value"].(string)
				encodedData[key] = base64.StdEncoding.EncodeToString([]byte(value))
			}
		}

	case "kubernetes.io/tls":
		d, ok := secret.Data.(map[string]interface{})
		if !ok {
			return "", errors.New("datos inválidos para Secret TLS")
		}
		tlsCrt := d["tls_crt"].(string)
		tlsKey := d["tls_key"].(string)
		encodedData["tls.crt"] = base64.StdEncoding.EncodeToString([]byte(tlsCrt))
		encodedData["tls.key"] = base64.StdEncoding.EncodeToString([]byte(tlsKey))

	case "kubernetes.io/dockerconfigjson":
		d, ok := secret.Data.(map[string]interface{})
		if !ok {
			return "", errors.New("datos inválidos para Secret Docker Config JSON")
		}
		config := d["dockerconfigjson"].(string)
		encodedData[".dockerconfigjson"] = base64.StdEncoding.EncodeToString([]byte(config))

	default:
		return "", errors.New("tipo de Secret no soportado")
	}

	secretYAML := map[string]interface{}{
		"apiVersion": "v1",
		"kind":       "Secret",
		"metadata": map[string]interface{}{
			"name":      secret.SecretName,
			"namespace": secret.Namespace,
		},
		"type": secret.SecretType,
		"data": encodedData,
	}

	out, err := yaml.Marshal(secretYAML)
	if err != nil {
		return "", err
	}
	return string(out), nil
}
