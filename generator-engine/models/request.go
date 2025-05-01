package models

type GenerateRequest struct {
	Namespace      *NamespaceObject      `json:"namespace,omitempty"`
	Deployment     *DeploymentObject     `json:"deployment,omitempty"`
	Service        *ServiceObject        `json:"service,omitempty"`
	HPA            *HPAObject            `json:"hpa,omitempty"`
	ConfigMap      *ConfigMapObject      `json:"configmap,omitempty"`
	Secret         *SecretObject         `json:"secret,omitempty"`
	PVC            *PVCObject            `json:"pvc,omitempty"`
	Ingress        *IngressObject        `json:"ingress,omitempty"`
	ServiceAccount *ServiceAccountObject `json:"serviceaccount,omitempty"`
	Role           *RoleObject           `json:"role,omitempty"`
	NetworkPolicy  *NetworkPolicyObject  `json:"networkPolicy,omitempty"`
}
