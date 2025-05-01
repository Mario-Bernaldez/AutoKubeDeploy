package models

type HPAMetric struct {
	ResourceName string `json:"resource_name"`
	TargetType   string `json:"target_type"`
	TargetValue  int    `json:"target_value"`
}

type HPAObject struct {
	HPAName          string      `json:"hpa_name"`
	Namespace        string      `json:"namespace"`
	TargetDeployment string      `json:"target_deployment"`
	MinReplicas      int         `json:"min_replicas"`
	MaxReplicas      int         `json:"max_replicas"`
	Metrics          []HPAMetric `json:"metrics"`
}
