package models

type NetworkPolicyRule struct {
	Direction     string            `json:"direction"` // "Ingress" o "Egress"
	Ports         []int             `json:"ports"`
	Selectors     map[string]string `json:"selectors"` // puede incluir podSelector, namespaceSelector, ipBlock
	IPBlockCIDR   string            `json:"cidr,omitempty"`
	IPBlockExcept []string          `json:"except,omitempty"`
}

type NetworkPolicyObject struct {
	Name        string              `json:"name"`
	Namespace   string              `json:"namespace"`
	PodSelector string              `json:"pod_selector"`
	PolicyTypes []string            `json:"policy_types"`
	Rules       []NetworkPolicyRule `json:"rules"`
}
