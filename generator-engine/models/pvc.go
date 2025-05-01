package models

type PVCObject struct {
	PVCName          string   `json:"pvc_name"`
	Namespace        string   `json:"namespace"`
	StorageRequest   string   `json:"storage_request"`
	AccessModes      []string `json:"access_modes"`
	StorageClassName string   `json:"storage_class_name"`
}
