from django.urls import path
from . import views


urlpatterns = [
    path("", views.redirect_to_configure, name="home"),
    path("configure/", views.object_selector, name="object_selector"),
    path(
        "configure/deployment/",
        views.deployment_config_view,
        name="configure_deployment",
    ),
    path("configure/service/", views.service_config_view, name="configure_service"),
    path(
        "configure/namespace/", views.namespace_config_view, name="configure_namespace"
    ),
    path("configure/hpa/", views.hpa_config_view, name="configure_hpa"),
    path(
        "configure/configMap/", views.configmap_config_view, name="configure_configmap"
    ),
    path("configure/secret/", views.secret_config_view, name="configure_secret"),
    path("configure/pvc/", views.pvc_config_view, name="configure_pvc"),
    path("configure/ingress/", views.ingress_config_view, name="configure_ingress"),
    path(
        "configure/serviceaccount/",
        views.service_account_config_view,
        name="configure_service_account",
    ),
    path("configure/rbac/", views.rbac_config_view, name="configure_rbac"),
    path(
        "configure/networkpolicy/",
        views.networkpolicy_config_view,
        name="configure_network_policy",
    ),
    path("explain/", views.explain_yaml_view, name="explain_yaml"),
]
