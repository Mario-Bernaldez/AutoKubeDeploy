package models

type ServiceAccountObject struct {
	ServiceAccountName string   `json:"service_account_name"`
	Namespace          string   `json:"namespace"`
	ImagePullSecrets   []string `json:"imagePullSecrets"`
}
