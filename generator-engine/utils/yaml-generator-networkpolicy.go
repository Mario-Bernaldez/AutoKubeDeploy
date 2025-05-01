package utils

import (
	"generator-engine/models"
	"gopkg.in/yaml.v2"
)

func GenerateNetworkPolicyYAML(np models.NetworkPolicyObject) (string, error) {
	// Convertir el podSelector principal
	podSelector := parseLabels(np.PodSelector)

	spec := map[string]interface{}{
		"podSelector": map[string]interface{}{"matchLabels": podSelector},
		"policyTypes": np.PolicyTypes,
	}

	ingressRules := make([]map[string]interface{}, 0)
	egressRules := make([]map[string]interface{}, 0)

	for _, rule := range np.Rules {
		ruleEntry := map[string]interface{}{}

		// Puertos
		if len(rule.Ports) > 0 {
			ports := make([]map[string]interface{}, 0)
			for _, p := range rule.Ports {
				ports = append(ports, map[string]interface{}{
					"port": p,
				})
			}
			ruleEntry["ports"] = ports
		}

		// Selectores
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

		if len(peers) > 0 {
			if rule.Direction == "Ingress" {
				ruleEntry["from"] = peers
			} else {
				ruleEntry["to"] = peers
			}
		}

		if rule.Direction == "Ingress" {
			ingressRules = append(ingressRules, ruleEntry)
		} else {
			egressRules = append(egressRules, ruleEntry)
		}
	}

	if len(ingressRules) > 0 {
		spec["ingress"] = ingressRules
	}
	if len(egressRules) > 0 {
		spec["egress"] = egressRules
	}

	networkPolicy := map[string]interface{}{
		"apiVersion": "networking.k8s.io/v1",
		"kind":       "NetworkPolicy",
		"metadata": map[string]interface{}{
			"name":      np.Name,
			"namespace": np.Namespace,
		},
		"spec": spec,
	}

	out, err := yaml.Marshal(networkPolicy)
	if err != nil {
		return "", err
	}
	return string(out), nil
}
