package k8s

import (
    "context"
    "fmt"
    "strings"

    "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime/schema"
    "k8s.io/apimachinery/pkg/api/meta"
    "k8s.io/client-go/discovery"
    "k8s.io/client-go/discovery/cached/memory"
    "k8s.io/client-go/dynamic"
    "k8s.io/client-go/rest"
    "k8s.io/client-go/restmapper"
)

func ListResourceNames(resource string, namespace string) ([]string, error) {
    config, err := rest.InClusterConfig()
    if err != nil {
        return nil, fmt.Errorf("error cargando configuración del clúster: %w", err)
    }

    client, err := dynamic.NewForConfig(config)
    if err != nil {
        return nil, fmt.Errorf("error creando cliente dinámico: %w", err)
    }

    mapper := restMapper(config)

    gvr, err := resolveGVR(mapper, resource)
    if err != nil {
        return nil, fmt.Errorf("error resolviendo GVR: %w", err)
    }

    var ri dynamic.ResourceInterface
    if gvr.Resource == "namespaces" || namespace == "" {
        ri = client.Resource(gvr)
    } else {
        ri = client.Resource(gvr).Namespace(namespace)
    }

    list, err := ri.List(context.Background(), v1.ListOptions{})
    if err != nil {
        return nil, fmt.Errorf("error listando recursos: %w", err)
    }

    names := []string{}
    for _, item := range list.Items {
        names = append(names, item.GetName())
    }

    return names, nil
}

func resolveGVR(mapper meta.RESTMapper, resource string) (schema.GroupVersionResource, error) {
    resource = strings.ToLower(resource)
    gk := schema.GroupKind{Kind: resource}
    mappings, err := mapper.RESTMappings(gk)
    if err != nil {
        return schema.GroupVersionResource{}, err
    }
    return mappings[0].Resource, nil
}
