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
    path("explain/", views.explain_yaml_view, name="explain_yaml"),
]
