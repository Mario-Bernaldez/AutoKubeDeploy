package handlers

import (
    "encoding/json"
    "net/http"

    "kube-manager/src"
)

func ListHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	resource := r.URL.Query().Get("resource")
	namespace := r.URL.Query().Get("namespace")

	if resource == "" {
		http.Error(w, "Missing 'resource' parameter", http.StatusBadRequest)
		return
	}

	resources, err := k8s.ListResources(resource, namespace)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resources)
}
