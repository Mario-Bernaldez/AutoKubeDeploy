package handlers

import (
    "fmt"
    "io"
    "net/http"

    "kube-manager/src/k8s"
)

func DeployHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Método no permitido", http.StatusMethodNotAllowed)
        return
    }

    body, err := io.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Error leyendo el cuerpo", http.StatusBadRequest)
        return
    }

    err = k8s.ApplyYAML(body)
    if err != nil {
        http.Error(w, fmt.Sprintf("Error desplegando YAML: %v", err), http.StatusInternalServerError)
        return
    }

    fmt.Fprintln(w, "YAML desplegado exitosamente")
}
