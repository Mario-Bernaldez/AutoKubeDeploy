package utils

import (
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GenerateServiceYAML(svc models.ServiceObject) (string, error) {
	selector := parseLabels(svc.Selector)

	// Build the list of ports
	ports := make([]map[string]interface{}, 0)
	for _, p := range svc.Ports {
		portEntry := map[string]interface{}{
			"port":       p.Port,
			"targetPort": p.TargetPort,
			"protocol":   p.Protocol,
		}
		// Include nodePort only if it's a NodePort service and value is not zero
		if svc.ServiceType == "NodePort" && p.NodePort != 0 {
			portEntry["nodePort"] = p.NodePort
		}
		ports = append(ports, portEntry)
	}

	metadata := map[string]interface{}{
		"name": svc.ServiceName,
	}
	if svc.Namespace != "" {
		metadata["namespace"] = svc.Namespace
	}

	serviceYAML := map[string]interface{}{
		"apiVersion": "v1",
		"kind":       "Service",
		"metadata":   metadata,
		"spec": map[string]interface{}{
			"type":     svc.ServiceType,
			"selector": selector,
			"ports":    ports,
		},
	}

	out, err := yaml.Marshal(serviceYAML)
	if err != nil {
		return "", err
	}
	return string(out), nil
}
