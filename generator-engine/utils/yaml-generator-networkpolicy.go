package utils

import (
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GenerateNetworkPolicyYAML(np models.NetworkPolicyObject) (string, error) {
	podSelector := parseLabels(np.PodSelector)

	spec := map[string]interface{}{
		"podSelector": map[string]interface{}{"matchLabels": podSelector},
		"policyTypes": np.PolicyTypes,
	}

	ingressRules := make([]map[string]interface{}, 0)
	egressRules := make([]map[string]interface{}, 0)

	for _, rule := range np.Rules {
		ruleEntry := map[string]interface{}{}

		// Ports
		if len(rule.Ports) > 0 {
			ports := make([]map[string]interface{}, 0)
			for _, p := range rule.Ports {
				ports = append(ports, map[string]interface{}{
					"port": p,
				})
			}
			ruleEntry["ports"] = ports
		}

		// Selectors
		peers := make([]map[string]interface{}, 0)

		if val, ok := rule.Selectors["podSelector"]; ok && val != "" {
			peers = append(peers, map[string]interface{}{
				"podSelector": map[string]interface{}{
					"matchLabels": parseLabels(val),
				},
			})
		}
		if val, ok := rule.Selectors["namespaceSelector"]; ok && val != "" {
			peers = append(peers, map[string]interface{}{
				"namespaceSelector": map[string]interface{}{
					"matchLabels": parseLabels(val),
				},
			})
		}
		if val, ok := rule.Selectors["ipBlock"]; ok && val != "" {
			ipBlock := map[string]interface{}{
				"cidr": val,
			}
			if len(rule.IPBlockExcept) > 0 {
				ipBlock["except"] = rule.IPBlockExcept
			}
			peers = append(peers, map[string]interface{}{
				"ipBlock": ipBlock,
			})
		}

		// Ingress
		if rule.Direction == "Ingress" {
			if len(peers) > 0 {
				ruleEntry["from"] = peers
			}
			if len(peers) > 0 || len(rule.Ports) > 0 {
				ingressRules = append(ingressRules, ruleEntry)
			}
		}

		// Egress
		if rule.Direction == "Egress" {
			if len(peers) > 0 {
				ruleEntry["to"] = peers
			}
			if len(peers) > 0 || len(rule.Ports) > 0 {
				egressRules = append(egressRules, ruleEntry)
			}
		}
	}

	if len(ingressRules) > 0 {
		spec["ingress"] = ingressRules
	}
	if len(egressRules) > 0 {
		spec["egress"] = egressRules
	}

	namespace := np.Namespace
	if namespace == "" {
		namespace = "default"
	}

	networkPolicy := map[string]interface{}{
		"apiVersion": "networking.k8s.io/v1",
		"kind":       "NetworkPolicy",
		"metadata": map[string]interface{}{
			"name":      np.Name,
			"namespace": namespace,
		},
		"spec": spec,
	}

	out, err := yaml.Marshal(networkPolicy)
	if err != nil {
		return "", err
	}
	return string(out), nil
}

func contains(slice []string, val string) bool {
	for _, s := range slice {
		if s == val {
			return true
		}
	}
	return false
}
