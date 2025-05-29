package utils

import (
	"strconv"
	"strings"

	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func parseIntOrString(value string) interface{} {
	// Try to convert to integer
	if i, err := strconv.Atoi(value); err == nil {
		return i
	}
	// If not an integer, return the string as is
	return value
}

func GenerateDeploymentYAML(dep models.DeploymentObject) (string, error) {
	podLabels := parseLabels(dep.PodTemplate.Labels)

	containers := make([]map[string]interface{}, 0)
	initContainers := make([]map[string]interface{}, 0)

	for _, container := range dep.Containers {
		portList := make([]map[string]int, 0)
		portStrs := strings.Split(container.Ports, ",")
		for _, p := range portStrs {
			p = strings.TrimSpace(p)
			if p == "" {
				continue
			}
			portInt, err := strconv.Atoi(p)
			if err == nil {
				portList = append(portList, map[string]int{
					"containerPort": portInt,
				})
			}
		}

		// Process environment variables
		envMap := parseEnvVars(container.EnvVars)
		envVarsList := make([]map[string]string, 0)
		for k, v := range envMap {
			envVarsList = append(envVarsList, map[string]string{
				"name":  k,
				"value": v,
			})
		}

		// Process container-specific volumeMounts
		volumeMounts := make([]map[string]interface{}, 0)
		for _, vm := range container.VolumeMounts {
			volumeMounts = append(volumeMounts, map[string]interface{}{
				"name":      vm.VolumeName,
				"mountPath": vm.MountPath,
			})
		}

		c := map[string]interface{}{
			"name":            container.ContainerName,
			"image":           container.Image,
			"imagePullPolicy": container.ImagePullPolicy,
			"ports":           portList,
			"env":             envVarsList,
			"volumeMounts":    volumeMounts,
		}

		if len(container.Command) > 0 {
			c["command"] = container.Command
		}


		if container.InitContainer {
			initContainers = append(initContainers, c)
		} else {
			containers = append(containers, c)
		}
	}

	volumes := make([]map[string]interface{}, 0)
	for _, volume := range dep.Volumes {
		switch volume.VolumeType {
		case "emptyDir":
			emptyDir := map[string]interface{}{}
			if volume.Medium != "" {
				emptyDir["medium"] = volume.Medium
			}
			if volume.SizeLimit != "" {
				emptyDir["sizeLimit"] = volume.SizeLimit
			}
			volumes = append(volumes, map[string]interface{}{
				"name":     volume.VolumeName,
				"emptyDir": emptyDir,
			})

		case "hostPath":
			if volume.Path != "" {
				hostPath := map[string]interface{}{
					"path": volume.Path,
				}
				if volume.HostpathType != "" {
					hostPath["type"] = volume.HostpathType
				}
				volumes = append(volumes, map[string]interface{}{
					"name":     volume.VolumeName,
					"hostPath": hostPath,
				})
			}

		case "configMap":
			if volume.ConfigMapName != "" {
				volumes = append(volumes, map[string]interface{}{
					"name": volume.VolumeName,
					"configMap": map[string]interface{}{
						"name": volume.ConfigMapName,
					},
				})
			}

		case "secret":
			if volume.SecretName != "" {
				volumes = append(volumes, map[string]interface{}{
					"name": volume.VolumeName,
					"secret": map[string]interface{}{
						"secretName": volume.SecretName,
					},
				})
			}

		case "pvc":
			if volume.PvcClaimName != "" {
				volumes = append(volumes, map[string]interface{}{
					"name": volume.VolumeName,
					"persistentVolumeClaim": map[string]interface{}{
						"claimName": volume.PvcClaimName,
					},
				})
			}
		}
	}

	podSpec := map[string]interface{}{
		"containers": containers,
		"volumes":    volumes,
	}
	if len(initContainers) > 0 {
		podSpec["initContainers"] = initContainers
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
					"maxUnavailable": parseIntOrString(dep.Deployment.MaxUnavailable),
					"maxSurge":       parseIntOrString(dep.Deployment.MaxSurge),
				},
			},
			"selector": map[string]interface{}{
				"matchLabels": podLabels,
			},
			"template": map[string]interface{}{
				"metadata": map[string]interface{}{
					"labels": podLabels,
				},
				"spec": podSpec,
			},
		},
	}

	out, err := yaml.Marshal(deploymentYAML)
	if err != nil {
		return "", err
	}
	return string(out), nil
}
