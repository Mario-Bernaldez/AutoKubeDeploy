from django.forms import formset_factory
from django.shortcuts import render
from django.http import JsonResponse
from .forms import (
    ObjectTypeForm, DeploymentForm, PodTemplateForm, ContainerForm,
    VolumeMountForm, VolumeForm, NamespaceForm, ServiceForm
)

def deployment_config_view(request):
    # Definir los formsets
    ContainerFormSet = formset_factory(ContainerForm, extra=1)
    VolumeFormSet = formset_factory(VolumeForm, extra=1)
    VolumeMountFormSet = formset_factory(VolumeMountForm, extra=1)
    
    if request.method == "POST":
        object_type_form = ObjectTypeForm(request.POST)
        if object_type_form.is_valid():
            obj_type = object_type_form.cleaned_data['object_type']
        else:
            obj_type = 'deployment'  # por defecto

        if obj_type == 'deployment':
            deployment_form = DeploymentForm(request.POST)
            pod_form = PodTemplateForm(request.POST)
            container_formset = ContainerFormSet(request.POST, prefix="containers")
            volume_formset = VolumeFormSet(request.POST, prefix="volumes")
            volume_mount_formset = VolumeMountFormSet(request.POST, prefix="volume_mounts")
            if (deployment_form.is_valid() and pod_form.is_valid() and 
                container_formset.is_valid() and volume_formset.is_valid() and 
                volume_mount_formset.is_valid()):
                user_input_data = {
                    "deployment": deployment_form.cleaned_data,
                    "pod_template": pod_form.cleaned_data,
                    "containers": [form.cleaned_data for form in container_formset],
                    "volumes": [form.cleaned_data for form in volume_formset],
                    "volume_mounts": [form.cleaned_data for form in volume_mount_formset]
                }
                return JsonResponse(user_input_data, json_dumps_params={'indent': 4})
        elif obj_type == 'namespace':
            namespace_form = NamespaceForm(request.POST)
            if namespace_form.is_valid():
                user_input_data = {
                    "namespace": namespace_form.cleaned_data
                }
                return JsonResponse(user_input_data, json_dumps_params={'indent': 4})
        elif obj_type == 'service':
            service_form = ServiceForm(request.POST)
            if service_form.is_valid():
                user_input_data = {
                    "service": service_form.cleaned_data
                }
                return JsonResponse(user_input_data, json_dumps_params={'indent': 4})
    else:
        object_type_form = ObjectTypeForm()
        # Instanciar todos los formularios, pero se mostrará solo uno según la selección
        deployment_form = DeploymentForm()
        pod_form = PodTemplateForm()
        container_formset = ContainerFormSet(prefix="containers")
        volume_formset = VolumeFormSet(prefix="volumes")
        volume_mount_formset = VolumeMountFormSet(prefix="volume_mounts")
        namespace_form = NamespaceForm()
        service_form = ServiceForm()
        obj_type = 'deployment'  # selección por defecto

    return render(request, "deployment_form.html", {
        "object_type_form": object_type_form,
        "selected_obj_type": obj_type,
        "deployment_form": deployment_form,
        "pod_form": pod_form,
        "container_formset": container_formset,
        "volume_formset": volume_formset,
        "volume_mount_formset": volume_mount_formset,
        "namespace_form": namespace_form,
        "service_form": service_form,
    })
