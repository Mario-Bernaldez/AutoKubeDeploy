from django.urls import path
from django.shortcuts import redirect
from .views import deployment_config_view

def redirect_to_configure(request):
    return redirect("configure_deployment")

urlpatterns = [
    path("", redirect_to_configure, name="home"),
    path("configure/", deployment_config_view, name="configure_deployment"),
]
5