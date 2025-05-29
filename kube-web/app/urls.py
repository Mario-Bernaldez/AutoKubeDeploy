from django.urls import path
from . import views


urlpatterns = [
    path("set_language/<str:language>", views.set_language, name="set_language"),
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
    path("apply/", views.apply_yaml, name="apply_yaml"),
    path("explore/", views.explore_resources, name="explore_resources"),
    path("delete-resource/", views.delete_resource, name="delete_resource"),
    path("history/", views.deployment_history_view, name="deployment_history"),
    path(
        "history/view/<int:pk>/",
        views.view_deployment_yaml,
        name="view_deployment_yaml",
    ),
]
