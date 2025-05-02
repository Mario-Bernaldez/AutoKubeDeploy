package k8s

import (
    "context"
    "fmt"

    "k8s.io/client-go/discovery"
    "k8s.io/client-go/dynamic"
    "k8s.io/client-go/kubernetes/scheme"
    "k8s.io/client-go/rest"
    "k8s.io/client-go/restmapper"
    "k8s.io/apimachinery/pkg/api/meta"
    "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
    "k8s.io/apimachinery/pkg/runtime/schema"
    "k8s.io/client-go/discovery/cached/memory"
    "k8s.io/apimachinery/pkg/runtime/serializer/yaml"
)

var decUnstructured = yaml.NewDecodingSerializer(unstructured.UnstructuredJSONScheme)

func ApplyYAML(yamlBytes []byte) error {
    config, err := rest.InClusterConfig()
    if err != nil {
        return fmt.Errorf("no se pudo cargar la configuración del clúster: %w", err)
    }

    client, err := dynamic.NewForConfig(config)
    if err != nil {
        return fmt.Errorf("error creando cliente dinámico: %w", err)
    }

    obj := &unstructured.Unstructured{}
    _, gvk, err := decUnstructured.Decode(yamlBytes, nil, obj)
    if err != nil {
        return fmt.Errorf("error decodificando YAML: %w", err)
    }

    mapper := restMapper(config)
    mapping, err := mapper.RESTMapping(schema.GroupKind{
        Group: gvk.Group,
        Kind:  gvk.Kind,
    }, gvk.Version)
    if err != nil {
        return fmt.Errorf("error obteniendo RESTMapping: %w", err)
    }

    resourceClient := client.Resource(mapping.Resource).Namespace(obj.GetNamespace())
    _, err = resourceClient.Create(context.Background(), obj, v1.CreateOptions{})
    if err != nil {
        return fmt.Errorf("error creando recurso en Kubernetes: %w", err)
    }

    return nil
}

func restMapper(config *rest.Config) meta.RESTMapper {
    dc, _ := discovery.NewDiscoveryClientForConfig(config)
    return restmapper.NewDeferredDiscoveryRESTMapper(memory.NewMemCacheClient(dc))
}
