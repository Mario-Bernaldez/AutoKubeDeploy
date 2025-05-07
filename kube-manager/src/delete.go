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
        return fmt.Errorf("error loading cluster configuration: %w", err)
    }

    client, err := dynamic.NewForConfig(config)
    if err != nil {
        return fmt.Errorf("error creating dynamic client: %w", err)
    }

    gvr, ok := resourceGVRMap[kind]
    if !ok {
        return fmt.Errorf("unsupported resource type: %s", kind)
    }

    var ri dynamic.ResourceInterface
    if gvr.Resource == "namespaces" || namespace == "" {
        ri = client.Resource(gvr)
    } else {
        ri = client.Resource(gvr).Namespace(namespace)
    }

    err = ri.Delete(context.Background(), name, metav1.DeleteOptions{})
    if err != nil {
        return fmt.Errorf("error deleting resource %s/%s: %w", kind, name, err)
    }

    return nil
}
