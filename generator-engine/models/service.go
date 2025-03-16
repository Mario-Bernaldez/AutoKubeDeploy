package models

// ServiceObject define la estructura para crear un Service en Kubernetes.
type ServiceObject struct {
	ServiceName string `json:"service_name"`
	ServiceType string `json:"service_type"`
	Ports       string `json:"ports"`
	Selector    string `json:"selector"`
}
