package utils

import (
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GenerateConfigMapYAML(cm models.ConfigMapObject) (string, error) {
	data := make(map[string]interface{})

	for _, key := range cm.Keys {
		if key.IsMultiline {
			data[key.KeyName] = key.Value // will be used as a multiline text block
		} else {
			data[key.KeyName] = key.Value // will be rendered inline
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
