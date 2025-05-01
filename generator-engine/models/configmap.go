package models

type ConfigMapKey struct {
	KeyName     string `json:"key_name"`
	IsMultiline bool   `json:"is_multiline"`
	Value       string `json:"value"`
}

type ConfigMapObject struct {
	ConfigMapName string         `json:"configmap_name"`
	Namespace     string         `json:"namespace"`
	Keys          []ConfigMapKey `json:"keys"`
}
