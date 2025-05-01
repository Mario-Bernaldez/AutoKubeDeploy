package utils

import (
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GenerateHPAYAML(hpa models.HPAObject) (string, error) {
	metrics := make([]map[string]interface{}, 0)
	for _, m := range hpa.Metrics {
		metric := map[string]interface{}{
			"type": "Resource",
			"resource": map[string]interface{}{
				"name": m.ResourceName,
				"target": map[string]interface{}{
					"type":  m.TargetType,
					"value": m.TargetValue,
				},
			},
		}
		if m.TargetType == "Utilization" {
			metric["resource"].(map[string]interface{})["target"] = map[string]interface{}{
				"type":               "Utilization",
				"averageUtilization": m.TargetValue,
			}
		} else {
			metric["resource"].(map[string]interface{})["target"] = map[string]interface{}{
				"type":         "Value",
				"averageValue": m.TargetValue,
			}
		}
		metrics = append(metrics, metric)
	}

	hpaYAML := map[string]interface{}{
		"apiVersion": "autoscaling/v2",
		"kind":       "HorizontalPodAutoscaler",
		"metadata": map[string]interface{}{
			"name":      hpa.HPAName,
			"namespace": hpa.Namespace,
		},
		"spec": map[string]interface{}{
			"scaleTargetRef": map[string]interface{}{
				"apiVersion": "apps/v1",
				"kind":       "Deployment",
				"name":       hpa.TargetDeployment,
			},
			"minReplicas": hpa.MinReplicas,
			"maxReplicas": hpa.MaxReplicas,
			"metrics":     metrics,
		},
	}

	out, err := yaml.Marshal(hpaYAML)
	if err != nil {
		return "", err
	}
	return string(out), nil
}
