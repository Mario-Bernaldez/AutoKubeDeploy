package handlers

import (
    "fmt"
    "net/http"

    "kube-manager/src"
)

func DeleteHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodDelete {
        http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
        return
    }

    resource := r.URL.Query().Get("type")
    name := r.URL.Query().Get("name")
    namespace := r.URL.Query().Get("namespace")

    if resource == "" || name == "" {
        http.Error(w, "Faltan parámetros 'type' o 'name'", http.StatusBadRequest)
        return
    }

    err := k8s.DeleteResource(resource, name, namespace)
    if err != nil {
        http.Error(w, fmt.Sprintf("Error al eliminar recurso: %v", err), http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusNoContent)
}
