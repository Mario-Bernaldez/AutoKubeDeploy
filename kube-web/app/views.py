import requests
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import (
    ObjectTypeForm, DeploymentForm, PodTemplateForm, ContainerForm,
    VolumeMountForm, VolumeForm, NamespaceForm, ServiceForm
)


def object_selector(request):
    if request.method == "POST":
        selected = request.POST.get("object_type")
        if selected == "deployment":
            return redirect("configure_deployment")
        elif selected == "service":
            return redirect("configure_service")
        elif selected == "namespace":
            return redirect("configure_namespace")
    return render(request, "object_selector.html")

def deployment_config_view(request):
    ContainerFormSet = formset_factory(ContainerForm, extra=1)
    VolumeFormSet = formset_factory(VolumeForm, extra=1)
    VolumeMountFormSet = formset_factory(VolumeMountForm, extra=1)

    if request.method == "POST":
        deployment_form = DeploymentForm(request.POST)
        pod_form = PodTemplateForm(request.POST)
        container_formset = ContainerFormSet(request.POST, prefix="containers")
        volume_formset = VolumeFormSet(request.POST, prefix="volumes")
        volume_mount_formset = VolumeMountFormSet(request.POST, prefix="volume_mounts")

        if (deployment_form.is_valid() and pod_form.is_valid() and 
            container_formset.is_valid() and volume_formset.is_valid() and 
            volume_mount_formset.is_valid()):

            user_input_data = { "deployment": {
                "deployment": deployment_form.cleaned_data,
                "pod_template": pod_form.cleaned_data,
                "containers": [form.cleaned_data for form in container_formset],
                "volumes": [form.cleaned_data for form in volume_formset],
                "volume_mounts": [form.cleaned_data for form in volume_mount_formset]
            }}

            response = requests.post("http://generator-engine/generate", json=user_input_data)
            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(request, "yaml_result.html", {
                    "yaml_output": yaml_output,
                    "explanation": None,
                    "models": models,
                    "default_model": default_model
                })
            else:
                return HttpResponse(f"Error en la API: {response.status_code}", status=response.status_code)

    else:
        deployment_form = DeploymentForm()
        pod_form = PodTemplateForm()
        container_formset = ContainerFormSet(prefix="containers")
        volume_formset = VolumeFormSet(prefix="volumes")
        volume_mount_formset = VolumeMountFormSet(prefix="volume_mounts")

    return render(request, "deployment_config.html", {
        "deployment_form": deployment_form,
        "pod_form": pod_form,
        "container_formset": container_formset,
        "volume_formset": volume_formset,
        "volume_mount_formset": volume_mount_formset,
    })

def service_config_view(request):
    if request.method == "POST":
        service_form = ServiceForm(request.POST)
        if service_form.is_valid():
            user_input_data = { "service": service_form.cleaned_data }

            response = requests.post("http://generator-engine/generate", json=user_input_data)
            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(request, "yaml_result.html", {
                    "yaml_output": yaml_output,
                    "explanation": None,
                    "models": models,
                    "default_model": default_model
                })
            else:
                return HttpResponse(f"Error en la API: {response.status_code}", status=response.status_code)
    else:
        service_form = ServiceForm()

    return render(request, "service_config.html", {
        "service_form": service_form
    })

def namespace_config_view(request):
    if request.method == "POST":
        namespace_form = NamespaceForm(request.POST)
        if namespace_form.is_valid():
            user_input_data = { "namespace": namespace_form.cleaned_data }

            response = requests.post("http://generator-engine/generate", json=user_input_data)
            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(request, "yaml_result.html", {
                    "yaml_output": yaml_output,
                    "explanation": None,
                    "models": models,
                    "default_model": default_model
                })
            else:
                return HttpResponse(f"Error en la API: {response.status_code}", status=response.status_code)
    else:
        namespace_form = NamespaceForm()

    return render(request, "namespace_config.html", {
        "namespace_form": namespace_form
    })

def explain_yaml_view(request):
    if request.method == "POST":
        yaml_output = request.POST.get("yaml_generated", "")
        selected_model = request.POST.get("selected_model", "")

        payload = {
            "yaml": yaml_output,
            "model": selected_model
        }

        explanation_response = requests.post("http://yaml-explainer:8080/explain", json=payload)

        if explanation_response.status_code == 200:
            explanation = explanation_response.json().get("explanation", "Sin explicación disponible.")
        elif explanation_response.status_code == 429:
            explanation = "⚠️ Modelo no disponible actualmente. Por favor, inténtelo de nuevo más tarde."
        elif explanation_response.status_code == 402:
            explanation = (
                "💳 Créditos insuficientes. "
                "Puedes añadir más en <a href='https://openrouter.ai/settings/credits' target='_blank'>OpenRouter</a> "
                "o utilizar un modelo gratuito."
            )
        else:
            explanation = f"❌ Error al obtener explicación: {explanation_response.status_code}"

        models, default_model = get_model_options()
        return render(request, "yaml_result.html", {
            "yaml_output": yaml_output,
            "explanation": explanation,
            "models": models,
            "selected_model": selected_model,
            "default_model": default_model
        })
    else:
        return redirect("configure_deployment")



def redirect_to_configure(request):
    return redirect("configure_deployment")

def get_model_options():
    try:
        response = requests.get("http://yaml-explainer:8080/models", timeout=5)
        if response.status_code == 200:
            models = response.json()
            default_model = next((m["id"] for m in models if m.get("free")), None)
            return models, default_model
    except Exception:
        pass
    return [], None
