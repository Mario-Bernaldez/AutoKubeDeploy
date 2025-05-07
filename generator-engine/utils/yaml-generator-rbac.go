package utils

import (
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GenerateRBACYAML(roleObj models.RoleObject) (string, error) {
	// Build Role or ClusterRole
	roleYAML := map[string]interface{}{
		"apiVersion": "rbac.authorization.k8s.io/v1",
		"kind":       roleObj.Type,
		"metadata": map[string]interface{}{
			"name": roleObj.Name,
		},
		"rules": roleObj.Rules,
	}

	if roleObj.Type == "Role" && roleObj.Namespace != "" {
		roleYAML["metadata"].(map[string]interface{})["namespace"] = roleObj.Namespace
	}

	// Build RoleBinding or ClusterRoleBinding
	bindingKind := "RoleBinding"
	if roleObj.Type == "ClusterRole" {
		bindingKind = "ClusterRoleBinding"
	}

	bindingYAML := map[string]interface{}{
		"apiVersion": "rbac.authorization.k8s.io/v1",
		"kind":       bindingKind,
		"metadata": map[string]interface{}{
			"name": roleObj.Binding.Name,
		},
		"subjects": roleObj.Binding.Subjects,
		"roleRef": map[string]interface{}{
			"apiGroup": "rbac.authorization.k8s.io",
			"kind":     roleObj.Type,
			"name":     roleObj.Name,
		},
	}

	if roleObj.Type == "Role" && roleObj.Binding.Namespace != "" {
		bindingYAML["metadata"].(map[string]interface{})["namespace"] = roleObj.Binding.Namespace
	}

	// Serialize both resources in the same YAML file with separator ---
	outRole, err := yaml.Marshal(roleYAML)
	if err != nil {
		return "", err
	}
	outBinding, err := yaml.Marshal(bindingYAML)
	if err != nil {
		return "", err
	}

	return string(outRole) + "---\n" + string(outBinding), nil
}
