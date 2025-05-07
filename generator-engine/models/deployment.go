package models

// DeploymentObject defines the structure to create a Deployment in Kubernetes.
type DeploymentObject struct {
	Deployment  DeploymentSpec  `json:"deployment"`
	PodTemplate PodTemplateSpec `json:"pod_template"`
	Containers  []Container     `json:"containers"`
	Volumes     []Volume        `json:"volumes"`
}

// DeploymentSpec contains the deployment details.
type DeploymentSpec struct {
	Name           string `json:"name"`
	Namespace      string `json:"namespace"`
	Replicas       int    `json:"replicas"`
	Strategy       string `json:"strategy"`
	MaxUnavailable string `json:"max_unavailable"`
	MaxSurge       string `json:"max_surge"`
}

// PodTemplateSpec contains the pod template details.
type PodTemplateSpec struct {
	PodName string `json:"pod_name"`
	Labels  string `json:"labels"`
}

// Container defines the structure of a container.
type Container struct {
	ContainerName   string        `json:"container_name"`
	Image           string        `json:"image"`
	ImagePullPolicy string        `json:"image_pull_policy"`
	Ports           string        `json:"ports"`
	EnvVars         string        `json:"env_vars"`
	VolumeMounts    []VolumeMount `json:"volume_mounts"`
}

// Volume defines the structure of a volume.
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

// VolumeMount defines the structure to mount a volume.
type VolumeMount struct {
	VolumeName string `json:"volume_name"`
	MountPath  string `json:"mount_path"`
}
