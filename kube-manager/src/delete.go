package k8s

import (
    "context"
    "fmt"

    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/client-go/dynamic"
    "k8s.io/client-go/rest"
)

func DeleteResource(kind, name, namespace string) error {
    config, err := rest.InClusterConfig()
    if err != nil {
        return fmt.Errorf("error cargando configuración del clúster: %w", err)
    }

    client, err := dynamic.NewForConfig(config)
    if err != nil {
        return fmt.Errorf("error creando cliente dinámico: %w", err)
    }

    gvr, ok := resourceGVRMap[kind]
    if !ok {
        return fmt.Errorf("tipo de recurso no soportado: %s", kind)
    }

    var ri dynamic.ResourceInterface
    if gvr.Resource == "namespaces" || namespace == "" {
        ri = client.Resource(gvr)
    } else {
        ri = client.Resource(gvr).Namespace(namespace)
    }

    err = ri.Delete(context.Background(), name, metav1.DeleteOptions{})
    if err != nil {
        return fmt.Errorf("error eliminando recurso %s/%s: %w", kind, name, err)
    }

    return nil
}
