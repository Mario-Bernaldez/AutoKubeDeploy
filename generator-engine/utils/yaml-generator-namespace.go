package utils

import (
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GenerateNamespaceYAML(ns models.NamespaceObject) (string, error) {
	namespaceYAML := map[string]interface{}{
		"apiVersion": "v1",
		"kind":       "Namespace",
		"metadata": map[string]interface{}{
			"name":   ns.NamespaceName,
			"labels": parseLabels(ns.Labels),
		},
	}
	out, err := yaml.Marshal(namespaceYAML)
	if err != nil {
		return "", err
	}
	return string(out), nil
}
