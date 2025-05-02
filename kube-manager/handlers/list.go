package handlers

import (
    "encoding/json"
    "net/http"
    "strings"

    "kube-manager/src/k8s"
)

func ListHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodGet {
        http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
        return
    }

    resource := r.URL.Query().Get("resource")
    namespace := r.URL.Query().Get("namespace")

    if resource == "" {
        http.Error(w, "Falta el parámetro 'resource'", http.StatusBadRequest)
        return
    }

    names, err := k8s.ListResourceNames(resource, namespace)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(names)
}
