from django.forms import formset_factory
from django.shortcuts import render
from django.http import JsonResponse
from .forms import DeploymentForm, PodTemplateForm, ContainerForm, VolumeMountForm, VolumeForm

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
            # Genera el JSON con los datos ingresados
            user_input_data = {
                "deployment": deployment_form.cleaned_data,
                "pod_template": pod_form.cleaned_data,
                "containers": [form.cleaned_data for form in container_formset],
                "volumes": [form.cleaned_data for form in volume_formset],
                "volume_mounts": [form.cleaned_data for form in volume_mount_formset]
            }
            return JsonResponse(user_input_data, json_dumps_params={'indent': 4})
    else:
        deployment_form = DeploymentForm()
        pod_form = PodTemplateForm()
        container_formset = ContainerFormSet(prefix="containers")
        volume_formset = VolumeFormSet(prefix="volumes")
        volume_mount_formset = VolumeMountFormSet(prefix="volume_mounts")

    return render(request, "deployment_form.html", {
        "deployment_form": deployment_form,
        "pod_form": pod_form,
        "container_formset": container_formset,
        "volume_formset": volume_formset,
        "volume_mount_formset": volume_mount_formset
    })
