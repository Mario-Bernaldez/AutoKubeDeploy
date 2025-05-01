package utils

import (
	"strings"
)

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
