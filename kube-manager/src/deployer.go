package k8s

import (
    "context"
    "fmt"
    "strings"

    "k8s.io/client-go/dynamic"
    "k8s.io/client-go/rest"
    "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
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

    kind := strings.Title(obj.GetKind())
    gvr, ok := resourceGVRMap[kind]
    if !ok {
        return fmt.Errorf("tipo de recurso no soportado: %s", kind)
    }

    // Validación opcional: asegurar coherencia entre YAML y mapa
    if gvk.Group != gvr.Group || gvk.Version != gvr.Version {
        return fmt.Errorf("la versión o grupo del recurso no coincide con el mapa: YAML=%s/%s, Mapa=%s/%s",
            gvk.Group, gvk.Version, gvr.Group, gvr.Version)
    }

    // Asignar namespace por defecto si no está definido y el recurso lo requiere
    ns := obj.GetNamespace()
    if ns == "" && gvr.Resource != "namespaces" && !strings.HasPrefix(gvr.Resource, "cluster") {
        ns = "default"
        obj.SetNamespace(ns)
    }

    var ri dynamic.ResourceInterface
    if gvr.Resource == "namespaces" || ns == "" {
        ri = client.Resource(gvr)
    } else {
        ri = client.Resource(gvr).Namespace(ns)
    }

    _, err = ri.Create(context.Background(), obj, v1.CreateOptions{})
    if err != nil {
        return fmt.Errorf("error creando recurso en Kubernetes: %w", err)
    }

    return nil
}
