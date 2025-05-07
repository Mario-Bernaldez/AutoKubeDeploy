package handlers

import (
    "fmt"
    "io"
    "net/http"

    "kube-manager/src"
)

func DeployHandler(w http.ResponseWriter, r *http.Request) {
    if r.Method != http.MethodPost {
        http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
        return
    }

    body, err := io.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Error reading request body", http.StatusBadRequest)
        return
    }

    err = k8s.ApplyYAML(body)
    if err != nil {
        http.Error(w, fmt.Sprintf("Error applying YAML: %v", err), http.StatusInternalServerError)
        return
    }

    fmt.Fprintln(w, "YAML successfully deployed")
}
