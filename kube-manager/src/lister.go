package k8s

import (
    "context"
    "errors"
    "fmt"

    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime/schema"
    "k8s.io/client-go/dynamic"
    "k8s.io/client-go/rest"
)

func ListResourceNames(kind string, namespace string) ([]string, error) {
    config, err := rest.InClusterConfig()
    if err != nil {
        return nil, fmt.Errorf("error cargando configuración del clúster: %w", err)
    }

    client, err := dynamic.NewForConfig(config)
    if err != nil {
        return nil, fmt.Errorf("error creando cliente dinámico: %w", err)
    }

    gvr, err := resolveGVRStatic(kind)
    if err != nil {
        return nil, fmt.Errorf("error resolviendo GVR estático: %w", err)
    }

    var ri dynamic.ResourceInterface
    if gvr.Resource == "namespaces" || namespace == "" {
        ri = client.Resource(gvr)
    } else {
        ri = client.Resource(gvr).Namespace(namespace)
    }

    list, err := ri.List(context.Background(), metav1.ListOptions{})
    if err != nil {
        return nil, fmt.Errorf("error listando recursos: %w", err)
    }

    names := []string{}
    for _, item := range list.Items {
        names = append(names, item.GetName())
    }

    return names, nil
}

func resolveGVRStatic(kind string) (schema.GroupVersionResource, error) {
    if gvr, ok := resourceGVRMap[kind]; ok {
        return gvr, nil
    }
    return schema.GroupVersionResource{}, errors.New("tipo de recurso no reconocido o no soportado")
}
