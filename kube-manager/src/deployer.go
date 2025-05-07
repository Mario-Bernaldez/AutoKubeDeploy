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
        return fmt.Errorf("failed to load cluster configuration: %w", err)
    }

    client, err := dynamic.NewForConfig(config)
    if err != nil {
        return fmt.Errorf("error creating dynamic client: %w", err)
    }

    obj := &unstructured.Unstructured{}
    _, gvk, err := decUnstructured.Decode(yamlBytes, nil, obj)
    if err != nil {
        return fmt.Errorf("error decoding YAML: %w", err)
    }

    kind := strings.Title(obj.GetKind())
    gvr, ok := resourceGVRMap[kind]
    if !ok {
        return fmt.Errorf("unsupported resource type: %s", kind)
    }

    // Optional validation: ensure consistency between YAML and GVR map
    if gvk.Group != gvr.Group || gvk.Version != gvr.Version {
        return fmt.Errorf("resource group or version mismatch: YAML=%s/%s, Map=%s/%s",
            gvk.Group, gvk.Version, gvr.Group, gvr.Version)
    }

    // Assign default namespace if not set and the resource requires one
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
        return fmt.Errorf("error creating resource in Kubernetes: %w", err)
    }

    return nil
}
