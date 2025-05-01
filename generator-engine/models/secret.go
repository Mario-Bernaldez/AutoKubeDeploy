package models

type SecretKey struct {
	KeyName string `json:"key_name"`
	Value   string `json:"value"`
}

type TLSSecretData struct {
	TLSCrt string `json:"tls_crt"`
	TLSKey string `json:"tls_key"`
}

type DockerConfigJSON struct {
	DockerConfigJSON string `json:"dockerconfigjson"`
}

type SecretObject struct {
	SecretName string      `json:"secret_name"`
	Namespace  string      `json:"namespace"`
	SecretType string      `json:"secret_type"`
	Data       interface{} `json:"data"` // puede ser []SecretKey, TLSSecretData, o DockerConfigJSON
}
