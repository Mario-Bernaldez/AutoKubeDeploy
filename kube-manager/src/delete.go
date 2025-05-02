package k8s

import (
    "context"
    "fmt"
    "strings"

    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime/schema"
    "k8s.io/client-go/discovery"
    "k8s.io/client-go/discovery/cached/memory"
    "k8s.io/client-go/dynamic"
    "k8s.io/client-go/rest"
    "k8s.io/client-go/restmapper"
)

func DeleteResource(kind, name, namespace string) error {
    config, err := rest.InClusterConfig()
    if err != nil {
        return fmt.Errorf("error cargando configuración: %w", err)
    }

    client, err := dynamic.NewForConfig(config)
    if err != nil {
        return fmt.Errorf("error creando cliente dinámico: %w", err)
    }

    mapper := restmapper.NewDeferredDiscoveryRESTMapper(memory.NewMemCacheClient(
        discovery.NewDiscoveryClientForConfigOrDie(config),
    ))

    gk := schema.GroupKind{Kind: strings.Title(kind)}
    mapping, err := mapper.RESTMapping(gk)
    if err != nil {
        return fmt.Errorf("error mapeando recurso: %w", err)
    }

    ri := client.Resource(mapping.Resource)
    if mapping.Scope.Name() != meta.RESTScopeNameRoot {
        ri = ri.Namespace(namespace)
    }

    return ri.Delete(context.Background(), name, metav1.DeleteOptions{})
}
