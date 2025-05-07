package utils

import (
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GeneratePVCYAML(pvc models.PVCObject) (string, error) {
	pvcYAML := map[string]interface{}{
		"apiVersion": "v1",
		"kind":       "PersistentVolumeClaim",
		"metadata": map[string]interface{}{
			"name":      pvc.PVCName,
			"namespace": pvc.Namespace,
		},
		"spec": map[string]interface{}{
			"accessModes": pvc.AccessModes,
			"resources": map[string]interface{}{
				"requests": map[string]string{
					"storage": pvc.StorageRequest,
				},
			},
		},
	}

	// Only add storageClassName if provided
	if pvc.StorageClassName != "" {
		pvcYAML["spec"].(map[string]interface{})["storageClassName"] = pvc.StorageClassName
	}

	out, err := yaml.Marshal(pvcYAML)
	if err != nil {
		return "", err
	}
	return string(out), nil
}
