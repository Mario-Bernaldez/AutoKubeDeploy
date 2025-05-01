package models

// DeploymentObject define la estructura para crear un Deployment en Kubernetes.
type DeploymentObject struct {
	Deployment  DeploymentSpec  `json:"deployment"`
	PodTemplate PodTemplateSpec `json:"pod_template"`
	Containers  []Container     `json:"containers"`
	Volumes     []Volume        `json:"volumes"`
}

// DeploymentSpec contiene los datos del deployment.
type DeploymentSpec struct {
	Name           string `json:"name"`
	Namespace      string `json:"namespace"`
	Replicas       int    `json:"replicas"`
	Strategy       string `json:"strategy"`
	MaxUnavailable string    `json:"max_unavailable"`
	MaxSurge       string    `json:"max_surge"`
}

// PodTemplateSpec contiene los datos de la plantilla de pod.
type PodTemplateSpec struct {
	PodName string `json:"pod_name"`
	Labels  string `json:"labels"`
}

// Container define la estructura de un contenedor.
type Container struct {
	ContainerName   string        `json:"container_name"`
	Image           string        `json:"image"`
	ImagePullPolicy string        `json:"image_pull_policy"`
	Ports           string        `json:"ports"`
	EnvVars         string        `json:"env_vars"`
	VolumeMounts    []VolumeMount `json:"volume_mounts"`
}

// Volume define la estructura de un volumen.
type Volume struct {
	VolumeName     string `json:"volume_name"`
	VolumeType     string `json:"volume_type"`
	Medium         string `json:"medium"`
	SizeLimit      string `json:"size_limit"`
	Path           string `json:"path"`
	HostpathType   string `json:"hostpath_type"`
	ConfigMapName  string `json:"config_map_name"`
	SecretName     string `json:"secret_name"`
	PvcClaimName   string `json:"pvc_claim_name"`
}

// VolumeMount define la estructura para montar un volumen.
type VolumeMount struct {
	VolumeName string `json:"volume_name"`
	MountPath  string `json:"mount_path"`
}
