from django.urls import path
from . import views

urlpatterns = [
    path("", views.redirect_to_configure, name="home"),
    path("configure/", views.deployment_config_view, name="configure_deployment"),
    path("explain/", views.explain_yaml_view, name="explain_yaml"),
]
