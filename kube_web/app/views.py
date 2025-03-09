from django.shortcuts import render
from django.http import JsonResponse
from .forms import DeploymentForm, PodTemplateForm, ContainerForm, VolumeMountForm, VolumeForm

def deployment_config_view(request):
    if request.method == "POST":
        deployment_form = DeploymentForm(request.POST)
        pod_form = PodTemplateForm(request.POST)
        container_form = ContainerForm(request.POST)
        volume_mount_form = VolumeMountForm(request.POST)
        volume_form = VolumeForm(request.POST)

        if all([deployment_form.is_valid(), pod_form.is_valid(), container_form.is_valid(), volume_mount_form.is_valid(), volume_form.is_valid()]):
            # Generación del JSON con los datos tal cual fueron ingresados
            user_input_data = {
                "deployment": deployment_form.cleaned_data,
                "pod_template": pod_form.cleaned_data,
                "container": container_form.cleaned_data,
                "volume_mount": volume_mount_form.cleaned_data,
                "volume": volume_form.cleaned_data
            }
            return JsonResponse(user_input_data, json_dumps_params={'indent': 4})

    else:
        deployment_form = DeploymentForm()
        pod_form = PodTemplateForm()
        container_form = ContainerForm()
        volume_mount_form = VolumeMountForm()
        volume_form = VolumeForm()

    return render(request, "deployment_form.html", {
        "deployment_form": deployment_form,
        "pod_form": pod_form,
        "container_form": container_form,
        "volume_mount_form": volume_mount_form,
        "volume_form": volume_form
    })
