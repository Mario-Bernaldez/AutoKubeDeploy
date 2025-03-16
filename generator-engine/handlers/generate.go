package handlers

import (
	"encoding/json"
	"io/ioutil"
	"net/http"

	"generator-engine/models"
	"generator-engine/utils"
)

// GenerateHandler procesa la petición POST en /generate y devuelve el YAML generado.
func GenerateHandler(w http.ResponseWriter, r *http.Request) {
	var req models.GenerateRequest

	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		http.Error(w, "Error leyendo el body de la petición", http.StatusBadRequest)
		return
	}

	err = json.Unmarshal(body, &req)
	if err != nil {
		http.Error(w, "Error al parsear JSON", http.StatusBadRequest)
		return
	}

	var yamlResult string
	if req.Namespace != nil {
		yamlResult, err = utils.GenerateNamespaceYAML(*req.Namespace)
		if err != nil {
			http.Error(w, "Error generando YAML para Namespace", http.StatusInternalServerError)
			return
		}
	} else if req.Deployment != nil {
		yamlResult, err = utils.GenerateDeploymentYAML(*req.Deployment)
		if err != nil {
			http.Error(w, "Error generando YAML para Deployment", http.StatusInternalServerError)
			return
		}
	} else if req.Service != nil {
		yamlResult, err = utils.GenerateServiceYAML(*req.Service)
		if err != nil {
			http.Error(w, "Error generando YAML para Service", http.StatusInternalServerError)
			return
		}
	} else {
		http.Error(w, "No se ha proporcionado un objeto Kubernetes válido", http.StatusBadRequest)
		return
	}

	w.Header().Set("Content-Type", "text/plain")
	w.Write([]byte(yamlResult))
}
