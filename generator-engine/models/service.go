package models

// ServicePort defines the structure of each port in the Service.
type ServicePort struct {
	Port       int    `json:"port"`
	TargetPort int    `json:"target_port"`
	Protocol   string `json:"protocol"`
	NodePort   int    `json:"node_port,omitempty"`
}

// ServiceObject defines the structure to create a Service in Kubernetes.
type ServiceObject struct {
	ServiceName string        `json:"service_name"`
	Namespace   string        `json:"namespace"`
	ServiceType string        `json:"service_type"`
	Ports       []ServicePort `json:"ports"`
	Selector    string        `json:"selector"`
}
