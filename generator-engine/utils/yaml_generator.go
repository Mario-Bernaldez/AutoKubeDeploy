package utils

import (
	"strconv"
	"strings"

	"gopkg.in/yaml.v2"
	"generator-engine/models" // reemplaza "your_module_path" por el path de tu módulo
)

// parseLabels convierte un string del tipo "key=value" en un mapa.
func parseLabels(labelsStr string) map[string]string {
	labels := make(map[string]string)
	parts := strings.Split(labelsStr, "=")
	if len(parts) == 2 {
		key := strings.TrimSpace(parts[0])
		value := strings.TrimSpace(parts[1])
		labels[key] = value
	}
	return labels
}

// parseEnvVars convierte un string del tipo "key=value" en un mapa.
func parseEnvVars(envStr string) map[string]string {
	env := make(map[string]string)
	parts := strings.Split(envStr, "=")
	if len(parts) == 2 {
		key := strings.TrimSpace(parts[0])
		value := strings.TrimSpace(parts[1])
		env[key] = value
	}
	return env
}

// GenerateNamespaceYAML genera el YAML para un Namespace.
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

// GenerateDeploymentYAML genera el YAML para un Deployment.
func GenerateDeploymentYAML(dep models.DeploymentObject) (string, error) {
	// Parsear las etiquetas del pod template.
	podLabels := parseLabels(dep.PodTemplate.Labels)

	// Construir la lista de volumeMounts (se asigna a todos los contenedores).
	volumeMounts := make([]map[string]interface{}, 0)
	for _, vm := range dep.VolumeMounts {
		volumeMounts = append(volumeMounts, map[string]interface{}{
			"name":      vm.VolumeName,
			"mountPath": vm.MountPath,
		})
	}

	// Construir la lista de contenedores.
	containers := make([]map[string]interface{}, 0)
	for _, container := range dep.Containers {
		portInt, _ := strconv.Atoi(container.Ports)
		envMap := parseEnvVars(container.EnvVars)
		envVarsList := make([]map[string]string, 0)
		for k, v := range envMap {
			envVarsList = append(envVarsList, map[string]string{
				"name":  k,
				"value": v,
			})
		}
		c := map[string]interface{}{
			"name":            container.ContainerName,
			"image":           container.Image,
			"imagePullPolicy": container.ImagePullPolicy,
			"ports": []map[string]int{
				{"containerPort": portInt},
			},
			"env":          envVarsList,
			"volumeMounts": volumeMounts,
		}
		containers = append(containers, c)
	}

	// Construir la lista de volúmenes (en este ejemplo solo se gestiona emptyDir).
	volumes := make([]map[string]interface{}, 0)
	for _, volume := range dep.Volumes {
		if volume.VolumeType == "emptyDir" {
			volumes = append(volumes, map[string]interface{}{
				"name":     volume.VolumeName,
				"emptyDir": map[string]interface{}{},
			})
		}
	}

	deploymentYAML := map[string]interface{}{
		"apiVersion": "apps/v1",
		"kind":       "Deployment",
		"metadata": map[string]interface{}{
			"name":      dep.Deployment.Name,
			"namespace": dep.Deployment.Namespace,
		},
		"spec": map[string]interface{}{
			"replicas": dep.Deployment.Replicas,
			"strategy": map[string]interface{}{
				"type": dep.Deployment.Strategy,
				"rollingUpdate": map[string]interface{}{
					"maxUnavailable": dep.Deployment.MaxUnavailable,
					"maxSurge":       dep.Deployment.MaxSurge,
				},
			},
			"template": map[string]interface{}{
				"metadata": map[string]interface{}{
					"labels": podLabels,
				},
				"spec": map[string]interface{}{
					"containers": containers,
					"volumes":    volumes,
				},
			},
		},
	}
	out, err := yaml.Marshal(deploymentYAML)
	if err != nil {
		return "", err
	}
	return string(out), nil
}

func GenerateServiceYAML(svc models.ServiceObject) (string, error) {
	selector := parseLabels(svc.Selector)
	portInt, err := strconv.Atoi(svc.Ports)
	if err != nil {
		portInt = 80
	}
	serviceYAML := map[string]interface{}{
		"apiVersion": "v1",
		"kind":       "Service",
		"metadata": map[string]interface{}{
			"name": svc.ServiceName,
		},
		"spec": map[string]interface{}{
			"type":     svc.ServiceType,
			"selector": selector,
			"ports": []map[string]interface{}{
				{"port": portInt},
			},
		},
	}
	out, err := yaml.Marshal(serviceYAML)
	if err != nil {
		return "", err
	}
	return string(out), nil
}
