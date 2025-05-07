package handlers

import (
    "fmt"
    "net/http"

    "kube-manager/src"
)

func DeleteHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodDelete {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    resource := r.URL.Query().Get("type")
    name := r.URL.Query().Get("name")
    namespace := r.URL.Query().Get("namespace")

    if resource == "" || name == "" {
        http.Error(w, "Missing 'type' or 'name' parameters", http.StatusBadRequest)
        return
    }

    err := k8s.DeleteResource(resource, name, namespace)
    if err != nil {
        http.Error(w, fmt.Sprintf("Error deleting resource: %v", err), http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusNoContent)
}
