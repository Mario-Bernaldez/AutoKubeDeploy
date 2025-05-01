package models

type IngressPath struct {
	Path        string `json:"path"`
	ServiceName string `json:"service_name"`
	ServicePort int    `json:"service_port"`
}

type IngressObject struct {
	IngressName string        `json:"ingress_name"`
	Namespace   string        `json:"namespace"`
	Host        string        `json:"host"`
	Paths       []IngressPath `json:"paths"`
}
