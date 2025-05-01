package utils

import (
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GenerateConfigMapYAML(cm models.ConfigMapObject) (string, error) {
	data := make(map[string]interface{})

	for _, key := range cm.Keys {
		if key.IsMultiline {
			data[key.KeyName] = key.Value // se usará como bloque de texto multilinea
		} else {
			data[key.KeyName] = key.Value // se renderiza inline
		}
	}

	configMapYAML := map[string]interface{}{
		"apiVersion": "v1",
		"kind":       "ConfigMap",
		"metadata": map[string]interface{}{
			"name":      cm.ConfigMapName,
			"namespace": cm.Namespace,
		},
		"data": data,
	}

	out, err := yaml.Marshal(configMapYAML)
	if err != nil {
		return "", err
	}
	return string(out), nil
}
