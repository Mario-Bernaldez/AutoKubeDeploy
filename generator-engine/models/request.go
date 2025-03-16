package models

type GenerateRequest struct {
	Namespace  *NamespaceObject  `json:"namespace,omitempty"`
	Deployment *DeploymentObject `json:"deployment,omitempty"`
	Service    *ServiceObject    `json:"service,omitempty"`
}
