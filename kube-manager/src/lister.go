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

type NamedResource struct {
	Name      string `json:"name"`
	Namespace string `json:"namespace"`
}

func ListResources(kind string, namespace string) ([]NamedResource, error) {
    config, err := rest.InClusterConfig()
    if err != nil {
        return nil, fmt.Errorf("error loading cluster configuration: %w", err)
    }

    client, err := dynamic.NewForConfig(config)
    if err != nil {
        return nil, fmt.Errorf("error creating dynamic client: %w", err)
    }

    gvr, err := resolveGVRStatic(kind)
    if err != nil {
        return nil, fmt.Errorf("error resolving static GVR: %w", err)
    }

    var ri dynamic.ResourceInterface
    if gvr.Resource == "namespaces" || namespace == "" {
        ri = client.Resource(gvr)
    } else {
        ri = client.Resource(gvr).Namespace(namespace)
    }

    list, err := ri.List(context.Background(), metav1.ListOptions{})
    if err != nil {
        return nil, fmt.Errorf("error listing resources: %w", err)
    }


    var result []NamedResource
    for _, item := range list.Items {
        ns := item.GetNamespace()
        if ns == "" {
            ns = "default"
        }
        result = append(result, NamedResource{
            Name:      item.GetName(),
            Namespace: ns,
        })
    }

    return result, nil
}

func resolveGVRStatic(kind string) (schema.GroupVersionResource, error) {
    if gvr, ok := resourceGVRMap[kind]; ok {
        return gvr, nil
    }
    return schema.GroupVersionResource{}, errors.New("unrecognized or unsupported resource type")
}
