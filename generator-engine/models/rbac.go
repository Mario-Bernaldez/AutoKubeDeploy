package models

type Rule struct {
	APIGroups []string `json:"apiGroups"`
	Resources []string `json:"resources"`
	Verbs     []string `json:"verbs"`
}

type Subject struct {
	Kind      string `json:"kind"`
	Name      string `json:"name"`
	Namespace string `json:"namespace,omitempty"` // only for ServiceAccount
}

type RoleBinding struct {
	Name      string    `json:"name"`
	Namespace string    `json:"namespace,omitempty"` // only for RoleBinding
	Subjects  []Subject `json:"subjects"`
}

type RoleObject struct {
	Type      string      `json:"type"` // "Role" or "ClusterRole"
	Name      string      `json:"name"`
	Namespace string      `json:"namespace,omitempty"` // only for Role
	Rules     []Rule      `json:"rules"`
	Binding   RoleBinding `json:"binding"`
}
