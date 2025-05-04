// resources.go
package k8s

import "k8s.io/apimachinery/pkg/runtime/schema"

var resourceGVRMap = map[string]schema.GroupVersionResource{
    "Pod": {
        Group:    "",
        Version:  "v1",
        Resource: "pods",
    },
    "Deployment": {
        Group:    "apps",
        Version:  "v1",
        Resource: "deployments",
    },
    "Service": {
        Group:    "",
        Version:  "v1",
        Resource: "services",
    },
    "Namespace": {
        Group:    "",
        Version:  "v1",
        Resource: "namespaces",
    },
    "HorizontalPodAutoscaler": {
        Group:    "autoscaling",
        Version:  "v2",
        Resource: "horizontalpodautoscalers",
    },
    "ConfigMap": {
        Group:    "",
        Version:  "v1",
        Resource: "configmaps",
    },
    "Secret": {
        Group:    "",
        Version:  "v1",
        Resource: "secrets",
    },
    "PersistentVolumeClaim": {
        Group:    "",
        Version:  "v1",
        Resource: "persistentvolumeclaims",
    },
    "Ingress": {
        Group:    "networking.k8s.io",
        Version:  "v1",
        Resource: "ingresses",
    },
    "ServiceAccount": {
        Group:    "",
        Version:  "v1",
        Resource: "serviceaccounts",
    },
    "Role": {
        Group:    "rbac.authorization.k8s.io",
        Version:  "v1",
        Resource: "roles",
    },
    "RoleBinding": {
        Group:    "rbac.authorization.k8s.io",
        Version:  "v1",
        Resource: "rolebindings",
    },
    "ClusterRole": {
        Group:    "rbac.authorization.k8s.io",
        Version:  "v1",
        Resource: "clusterroles",
    },
    "ClusterRoleBinding": {
        Group:    "rbac.authorization.k8s.io",
        Version:  "v1",
        Resource: "clusterrolebindings",
    },
    "NetworkPolicy": {
        Group:    "networking.k8s.io",
        Version:  "v1",
        Resource: "networkpolicies",
    },
}
