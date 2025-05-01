package models

// ServicePort define la estructura de cada puerto del Service.
type ServicePort struct {
	Port       int    `json:"port"`
	TargetPort int    `json:"target_port"`
	Protocol   string `json:"protocol"`
	NodePort   int    `json:"node_port,omitempty"`
}

// ServiceObject define la estructura para crear un Service en Kubernetes.
type ServiceObject struct {
	ServiceName string        `json:"service_name"`
	ServiceType string        `json:"service_type"`
	Ports       []ServicePort `json:"ports"`
	Selector    string        `json:"selector"`
}
