package handlers

import (
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"

	"generator-engine/models"
	"generator-engine/utils"
)

func GenerateHandler(w http.ResponseWriter, r *http.Request) {
	var req models.GenerateRequest

	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error reading request body", http.StatusBadRequest)
		return
	}

	err = json.Unmarshal(body, &req)
	if err != nil {
		log.Println("Error parsing JSON:", err)
		http.Error(w, "Error parsing JSON: "+err.Error(), http.StatusBadRequest)
		return
	}

	var yamlResult string
	if req.Namespace != nil {
		yamlResult, err = utils.GenerateNamespaceYAML(*req.Namespace)
		if err != nil {
			http.Error(w, "Error generating YAML for Namespace", http.StatusInternalServerError)
			return
		}
	} else if req.Deployment != nil {
		yamlResult, err = utils.GenerateDeploymentYAML(*req.Deployment)
		if err != nil {
			http.Error(w, "Error generating YAML for Deployment", http.StatusInternalServerError)
			return
		}
	} else if req.Service != nil {
		yamlResult, err = utils.GenerateServiceYAML(*req.Service)
		if err != nil {
			http.Error(w, "Error generating YAML for Service", http.StatusInternalServerError)
			return
		}
	} else if req.HPA != nil {
		yamlResult, err = utils.GenerateHPAYAML(*req.HPA)
		if err != nil {
			http.Error(w, "Error generating YAML for HPA", http.StatusInternalServerError)
			return
		}
	} else if req.ConfigMap != nil {
		yamlResult, err = utils.GenerateConfigMapYAML(*req.ConfigMap)
		if err != nil {
			http.Error(w, "Error generating YAML for ConfigMap", http.StatusInternalServerError)
			return
		}
	} else if req.Secret != nil {
		yamlResult, err = utils.GenerateSecretYAML(*req.Secret)
		if err != nil {
			http.Error(w, "Error generating YAML for Secret", http.StatusInternalServerError)
			return
		}
	} else if req.PVC != nil {
		yamlResult, err = utils.GeneratePVCYAML(*req.PVC)
		if err != nil {
			http.Error(w, "Error generating YAML for PersistentVolumeClaim", http.StatusInternalServerError)
			return
		}
	} else if req.Ingress != nil {
		yamlResult, err = utils.GenerateIngressYAML(*req.Ingress)
		if err != nil {
			http.Error(w, "Error generating YAML for Ingress", http.StatusInternalServerError)
			return
		}
	} else if req.ServiceAccount != nil {
		yamlResult, err = utils.GenerateServiceAccountYAML(*req.ServiceAccount)
		if err != nil {
			http.Error(w, "Error generating YAML for ServiceAccount", http.StatusInternalServerError)
			return
		}
	} else if req.Role != nil {
		yamlResult, err = utils.GenerateRBACYAML(*req.Role)
		if err != nil {
			http.Error(w, "Error generating YAML for Role/RoleBinding", http.StatusInternalServerError)
			return
		}
	} else {
		http.Error(w, "No valid Kubernetes object provided", http.StatusBadRequest)
		return
	}

	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte(yamlResult))
}
