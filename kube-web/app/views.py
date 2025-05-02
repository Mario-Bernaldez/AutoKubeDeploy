import requests
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import (
    ConfigMapForm,
    ConfigMapKeyForm,
    DeploymentForm,
    DockerConfigJSONForm,
    HPAForm,
    HPAMetricForm,
    ImagePullSecretForm,
    IngressForm,
    IngressPathForm,
    NetworkPolicyForm,
    NetworkRuleForm,
    OpaqueKeyForm,
    PersistentVolumeClaimForm,
    PodTemplateForm,
    ContainerForm,
    RoleBindingForm,
    RoleForm,
    RuleForm,
    SecretForm,
    ServiceAccountForm,
    ServicePortFormSet,
    SubjectForm,
    TLSSecretForm,
    VolumeMountForm,
    VolumeForm,
    NamespaceForm,
    ServiceForm,
    RequiredContainerFormSet,
)


def object_selector(request):
    if request.method == "POST":
        redirect_map = {
            "deployment": "configure_deployment",
            "service": "configure_service",
            "namespace": "configure_namespace",
            "hpa": "configure_hpa",
            "configMap": "configure_configmap",
            "secret": "configure_secret",
            "pvc": "configure_pvc",
            "ingress": "configure_ingress",
            "sa": "configure_service_account",
            "rbac": "configure_rbac",
            "networkpolicy": "configure_network_policy",
        }
        selected = request.POST.get("object_type")
        target = redirect_map.get(selected)
        if target:
            return redirect(target)
    return render(request, "object_selector.html")


def deployment_config_view(request):
    ContainerFormSet = formset_factory(
        ContainerForm, formset=RequiredContainerFormSet, extra=1
    )
    VolumeFormSet = formset_factory(VolumeForm, extra=1)
    VolumeMountFormSet = formset_factory(
        VolumeMountForm,
        extra=1,
    )

    if request.method == "POST":
        deployment_form = DeploymentForm(request.POST)
        pod_form = PodTemplateForm(request.POST)
        container_formset = ContainerFormSet(request.POST, prefix="containers")
        volume_formset = VolumeFormSet(request.POST, prefix="volumes")
        volume_mount_formset = VolumeMountFormSet(request.POST, prefix="volume_mounts")

        if (
            deployment_form.is_valid()
            and pod_form.is_valid()
            and container_formset.is_valid()
            and volume_formset.is_valid()
            and volume_mount_formset.is_valid()
        ):
            deployment_data = deployment_form.cleaned_data
            pod_data = pod_form.cleaned_data

            containers_data = []
            for idx, cform in enumerate(container_formset):
                c = cform.cleaned_data.copy()

                prefix = volume_mount_formset.prefix
                nombres = request.POST.getlist(f"{prefix}-{idx}-volume_name")
                rutas = request.POST.getlist(f"{prefix}-{idx}-mount_path")

                mounts = [
                    {"volume_name": name, "mount_path": path}
                    for name, path in zip(nombres, rutas)
                ]
                c["volume_mounts"] = mounts
                containers_data.append(c)

            volumes_data = [v.cleaned_data for v in volume_formset]

            user_input_data = {
                "deployment": {
                    "deployment": deployment_data,
                    "pod_template": pod_data,
                    "containers": containers_data,
                    "volumes": volumes_data,
                }
            }

            response = requests.post(
                "http://generator-engine/generate", json=user_input_data
            )
            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(
                    request,
                    "yaml_result.html",
                    {
                        "yaml_output": yaml_output,
                        "explanation": None,
                        "models": models,
                        "default_model": default_model,
                    },
                )
            else:
                return HttpResponse(
                    f"Error en la API: {response.status_code}",
                    status=response.status_code,
                )

    else:
        deployment_form = DeploymentForm()
        pod_form = PodTemplateForm()
        container_formset = ContainerFormSet(prefix="containers")
        volume_formset = VolumeFormSet(prefix="volumes")
        volume_mount_formset = VolumeMountFormSet(prefix="volume_mounts")

    return render(
        request,
        "deployment_config.html",
        {
            "deployment_form": deployment_form,
            "pod_form": pod_form,
            "container_formset": container_formset,
            "volume_formset": volume_formset,
            "volume_mount_formset": volume_mount_formset,
        },
    )


def service_config_view(request):
    if request.method == "POST":
        service_form = ServiceForm(request.POST)
        port_formset = ServicePortFormSet(request.POST, prefix="ports")

        if service_form.is_valid() and port_formset.is_valid():
            service_data = service_form.cleaned_data
            ports_data = [
                form.cleaned_data
                for form in port_formset.forms
                if not form.cleaned_data.get("DELETE", False)
            ]

            service_data["ports"] = ports_data
            user_input_data = {"service": service_data}

            response = requests.post(
                "http://generator-engine/generate", json=user_input_data
            )
            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(
                    request,
                    "yaml_result.html",
                    {
                        "yaml_output": yaml_output,
                        "explanation": None,
                        "models": models,
                        "default_model": default_model,
                    },
                )
            else:
                return HttpResponse(
                    f"Error en la API: {response.status_code}",
                    status=response.status_code,
                )
    else:
        service_form = ServiceForm()
        port_formset = ServicePortFormSet(prefix="ports")

    return render(
        request,
        "service_config.html",
        {
            "service_form": service_form,
            "port_formset": port_formset,
        },
    )


def namespace_config_view(request):
    if request.method == "POST":
        namespace_form = NamespaceForm(request.POST)
        if namespace_form.is_valid():
            user_input_data = {"namespace": namespace_form.cleaned_data}

            response = requests.post(
                "http://generator-engine/generate", json=user_input_data
            )
            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(
                    request,
                    "yaml_result.html",
                    {
                        "yaml_output": yaml_output,
                        "explanation": None,
                        "models": models,
                        "default_model": default_model,
                    },
                )
            else:
                return HttpResponse(
                    f"Error en la API: {response.status_code}",
                    status=response.status_code,
                )
    else:
        namespace_form = NamespaceForm()

    return render(request, "namespace_config.html", {"namespace_form": namespace_form})


def hpa_config_view(request):
    HPAMetricFormSet = formset_factory(HPAMetricForm, extra=1)
    if request.method == "POST":
        hpa_form = HPAForm(request.POST)
        metric_formset = HPAMetricFormSet(request.POST, prefix="metrics")

        if hpa_form.is_valid() and metric_formset.is_valid():
            metrics_data = [
                form.cleaned_data for form in metric_formset if form.cleaned_data
            ]
            hpa = hpa_form.cleaned_data
            hpa["metrics"] = metrics_data
            user_input_data = {"hpa": hpa}
            response = requests.post(
                "http://generator-engine/generate", json=user_input_data
            )
            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(
                    request,
                    "yaml_result.html",
                    {
                        "yaml_output": yaml_output,
                        "explanation": None,
                        "models": models,
                        "default_model": default_model,
                    },
                )
            else:
                return HttpResponse(
                    f"Error en la API: {response.status_code}",
                    status=response.status_code,
                )
    else:
        hpa_form = HPAForm()
        metric_formset = HPAMetricFormSet(prefix="metrics")

    return render(
        request,
        "hpa_config.html",
        {"hpa_form": hpa_form, "metric_formset": metric_formset},
    )


def configmap_config_view(request):
    ConfigMapKeyFormSet = formset_factory(ConfigMapKeyForm, extra=1)
    if request.method == "POST":
        configmap_form = ConfigMapForm(request.POST)
        configmap_key_formset = ConfigMapKeyFormSet(request.POST, prefix="properties")

        if configmap_form.is_valid() and configmap_key_formset.is_valid():
            keys_data = [
                form.cleaned_data for form in configmap_key_formset if form.cleaned_data
            ]
            configmap = configmap_form.cleaned_data
            configmap["keys"] = keys_data
            user_input_data = {"configmap": configmap}

            response = requests.post(
                "http://generator-engine/generate", json=user_input_data
            )
            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(
                    request,
                    "yaml_result.html",
                    {
                        "yaml_output": yaml_output,
                        "explanation": None,
                        "models": models,
                        "default_model": default_model,
                    },
                )
            else:
                return HttpResponse(
                    f"Error en la API: {response.status_code}",
                    status=response.status_code,
                )
    else:
        configmap_form = ConfigMapForm()
        configmap_key_formset = ConfigMapKeyFormSet(prefix="properties")

    return render(
        request,
        "configmap_config.html",
        {
            "configmap_form": configmap_form,
            "configmap_key_formset": configmap_key_formset,
        },
    )


def secret_config_view(request):
    OpaqueKeyFormSet = formset_factory(OpaqueKeyForm, extra=1)
    if request.method == "POST":
        secret_form = SecretForm(request.POST)
        opaque_formset = OpaqueKeyFormSet(request.POST, prefix="opaque")
        tls_form = TLSSecretForm(request.POST, prefix="tls")
        dockerconfigjson_form = DockerConfigJSONForm(request.POST, prefix="docker")

        if secret_form.is_valid():
            secret_type = secret_form.cleaned_data["secret_type"]

            data = secret_form.cleaned_data

            if secret_type == "Opaque":
                if opaque_formset.is_valid():
                    keys_data = [
                        form.cleaned_data
                        for form in opaque_formset
                        if form.cleaned_data
                    ]
                    data["data"] = keys_data
                else:
                    return render(
                        request,
                        "secret_config.html",
                        {
                            "secret_form": secret_form,
                            "opaque_formset": opaque_formset,
                            "tls_form": tls_form,
                            "dockerconfigjson_form": dockerconfigjson_form,
                        },
                    )

            elif secret_type == "kubernetes.io/tls":
                if tls_form.is_valid():
                    data["data"] = tls_form.cleaned_data
                else:
                    return render(
                        request,
                        "secret_config.html",
                        {
                            "secret_form": secret_form,
                            "opaque_formset": opaque_formset,
                            "tls_form": tls_form,
                            "dockerconfigjson_form": dockerconfigjson_form,
                        },
                    )

            elif secret_type == "kubernetes.io/dockerconfigjson":
                if dockerconfigjson_form.is_valid():
                    data["data"] = dockerconfigjson_form.cleaned_data
                else:
                    return render(
                        request,
                        "secret_config.html",
                        {
                            "secret_form": secret_form,
                            "opaque_formset": opaque_formset,
                            "tls_form": tls_form,
                            "dockerconfigjson_form": dockerconfigjson_form,
                        },
                    )
            user_input_data = {"secret": data}
            response = requests.post(
                "http://generator-engine/generate",
                json=user_input_data,
            )

            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(
                    request,
                    "yaml_result.html",
                    {
                        "yaml_output": yaml_output,
                        "explanation": None,
                        "models": models,
                        "default_model": default_model,
                    },
                )
            else:
                return HttpResponse(
                    f"Error en la API: {response.status_code}",
                    status=response.status_code,
                )

    else:
        secret_form = SecretForm()
        opaque_formset = OpaqueKeyFormSet(prefix="opaque")
        tls_form = TLSSecretForm(prefix="tls")
        dockerconfigjson_form = DockerConfigJSONForm(prefix="docker")

    return render(
        request,
        "secret_config.html",
        {
            "secret_form": secret_form,
            "opaque_formset": opaque_formset,
            "tls_form": tls_form,
            "dockerconfigjson_form": dockerconfigjson_form,
        },
    )


def pvc_config_view(request):
    if request.method == "POST":
        pvc_form = PersistentVolumeClaimForm(request.POST)

        if pvc_form.is_valid():
            user_input_data = {"pvc": pvc_form.cleaned_data}
            response = requests.post(
                "http://generator-engine/generate", json=user_input_data
            )
            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(
                    request,
                    "yaml_result.html",
                    {
                        "yaml_output": yaml_output,
                        "explanation": None,
                        "models": models,
                        "default_model": default_model,
                    },
                )
            else:
                return HttpResponse(
                    f"Error en la API: {response.status_code}",
                    status=response.status_code,
                )
    else:
        pvc_form = PersistentVolumeClaimForm()

    return render(request, "pvc_config.html", {"pvc_form": pvc_form})


def ingress_config_view(request):
    IngressPathFormSet = formset_factory(IngressPathForm, extra=1)
    if request.method == "POST":
        ingress_form = IngressForm(request.POST)
        path_formset = IngressPathFormSet(request.POST, prefix="paths")

        if ingress_form.is_valid() and path_formset.is_valid():
            paths_data = [
                form.cleaned_data for form in path_formset if form.cleaned_data
            ]
            ingress = ingress_form.cleaned_data
            ingress["paths"] = paths_data
            user_input_data = {"ingress": ingress}
            response = requests.post(
                "http://generator-engine/generate",
                json=user_input_data,
            )

            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(
                    request,
                    "yaml_result.html",
                    {
                        "yaml_output": yaml_output,
                        "explanation": None,
                        "models": models,
                        "default_model": default_model,
                    },
                )
            else:
                return HttpResponse(
                    f"Error en la API: {response.status_code}",
                    status=response.status_code,
                )
    else:
        ingress_form = IngressForm()
        path_formset = IngressPathFormSet(prefix="paths")

    return render(
        request,
        "ingress_config.html",
        {"ingress_form": ingress_form, "path_formset": path_formset},
    )


def service_account_config_view(request):
    ImagePullSecretFormSet = formset_factory(ImagePullSecretForm, extra=1)

    if request.method == "POST":
        serviceaccount_form = ServiceAccountForm(request.POST)
        imagepullsecret_formset = ImagePullSecretFormSet(
            request.POST, prefix="imagepullsecrets"
        )

        if serviceaccount_form.is_valid() and imagepullsecret_formset.is_valid():
            imagepullsecrets = [
                form.cleaned_data["secret_name"]
                for form in imagepullsecret_formset
                if form.cleaned_data
            ]
            serviceaccount = serviceaccount_form.cleaned_data
            serviceaccount["imagePullSecrets"] = imagepullsecrets
            user_input_data = {"serviceaccount": serviceaccount}
            response = requests.post(
                "http://generator-engine/generate",
                json=user_input_data,
            )

            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(
                    request,
                    "yaml_result.html",
                    {
                        "yaml_output": yaml_output,
                        "explanation": None,
                        "models": models,
                        "default_model": default_model,
                    },
                )
            else:
                return HttpResponse(
                    f"Error en la API: {response.status_code}",
                    status=response.status_code,
                )
    else:
        serviceaccount_form = ServiceAccountForm()
        imagepullsecret_formset = ImagePullSecretFormSet(prefix="imagepullsecrets")
    return render(
        request,
        "service_account_config.html",
        {
            "serviceaccount_form": serviceaccount_form,
            "imagepullsecret_formset": imagepullsecret_formset,
        },
    )


def rbac_config_view(request):
    RuleFormSet = formset_factory(RuleForm, extra=1)
    SubjectFormSet = formset_factory(SubjectForm, extra=1)
    if request.method == "POST":
        role_form = RoleForm(request.POST)
        rule_formset = RuleFormSet(request.POST, prefix="rules")
        rolebinding_form = RoleBindingForm(request.POST)
        subject_formset = SubjectFormSet(request.POST, prefix="subjects")

        if (
            role_form.is_valid()
            and rule_formset.is_valid()
            and rolebinding_form.is_valid()
            and subject_formset.is_valid()
        ):
            role_data = role_form.cleaned_data
            rules = []
            for form in rule_formset:
                if form.cleaned_data:
                    rules.append(
                        {
                            "apiGroups": [
                                g.strip()
                                for g in form.cleaned_data["api_groups"].split(",")
                                if g.strip()
                            ],
                            "resources": [
                                r.strip()
                                for r in form.cleaned_data["resources"].split(",")
                                if r.strip()
                            ],
                            "verbs": [
                                v.strip()
                                for v in form.cleaned_data["verbs"].split(",")
                                if v.strip()
                            ],
                        }
                    )

            binding_data = rolebinding_form.cleaned_data
            subjects = []
            for form in subject_formset:
                if form.cleaned_data:
                    subject = {
                        "kind": form.cleaned_data["kind"],
                        "name": form.cleaned_data["name"],
                    }
                    if form.cleaned_data["kind"] == "ServiceAccount":
                        subject["namespace"] = form.cleaned_data.get("namespace", "")
                    subjects.append(subject)

            payload = {
                "role": {
                    "type": role_data["role_type"],
                    "name": role_data["role_name"],
                    "namespace": role_data.get("namespace", ""),
                    "rules": rules,
                    "binding": {
                        "name": binding_data["binding_name"],
                        "namespace": binding_data.get("namespace", ""),
                        "subjects": subjects,
                    },
                },
            }
            response = requests.post("http://generator-engine/generate", json=payload)
            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(
                    request,
                    "yaml_result.html",
                    {
                        "yaml_output": yaml_output,
                        "explanation": None,
                        "models": models,
                        "default_model": default_model,
                    },
                )
            else:
                return HttpResponse(
                    f"Error en la API: {response.status_code}",
                    status=response.status_code,
                )

    else:
        role_form = RoleForm()
        rule_formset = RuleFormSet(prefix="rules")
        rolebinding_form = RoleBindingForm()
        subject_formset = SubjectFormSet(prefix="subjects")

    return render(
        request,
        "rbac_config.html",
        {
            "role_form": role_form,
            "rule_formset": rule_formset,
            "rolebinding_form": rolebinding_form,
            "subject_formset": subject_formset,
        },
    )


def networkpolicy_config_view(request):
    NetworkRuleFormSet = formset_factory(NetworkRuleForm, extra=1)
    if request.method == "POST":
        networkpolicy_form = NetworkPolicyForm(request.POST)
        rule_formset = NetworkRuleFormSet(request.POST, prefix="rules")

        if networkpolicy_form.is_valid() and rule_formset.is_valid():
            rules = []
            for form in rule_formset:
                if not form.cleaned_data:
                    continue
                rule = {
                    "direction": form.cleaned_data["direction"],
                    "ports": [],
                    "selectors": {},
                }

                # Procesar puertos
                ports_str = form.cleaned_data.get("ports", "")
                if ports_str:
                    rule["ports"] = [
                        int(p.strip())
                        for p in ports_str.split(",")
                        if p.strip().isdigit()
                    ]

                # Selectores
                if form.cleaned_data.get("pod_selector"):
                    rule["selectors"]["podSelector"] = form.cleaned_data["pod_selector"]
                if form.cleaned_data.get("namespace_selector"):
                    rule["selectors"]["namespaceSelector"] = form.cleaned_data[
                        "namespace_selector"
                    ]
                if form.cleaned_data.get("ip_block"):
                    rule["selectors"]["ipBlock"] = {
                        "cidr": form.cleaned_data["ip_block"],
                        "except": [
                            e.strip()
                            for e in form.cleaned_data.get("except_ips", "").split(",")
                            if e.strip()
                        ],
                    }

                rules.append(rule)

            networkPolicy = networkpolicy_form.cleaned_data
            networkPolicy["rules"] = rules
            payload = {"networkPolicy": networkPolicy}
            response = requests.post("http://generator-engine/generate", json=payload)

            if response.status_code == 200:
                yaml_output = response.text
                models, default_model = get_model_options()
                return render(
                    request,
                    "yaml_result.html",
                    {
                        "yaml_output": yaml_output,
                        "explanation": None,
                        "models": models,
                        "default_model": default_model,
                    },
                )
            else:
                return HttpResponse(
                    f"Error en la API: {response.status_code}",
                    status=response.status_code,
                )

    else:
        networkpolicy_form = NetworkPolicyForm()
        rule_formset = NetworkRuleFormSet(prefix="rules")

    return render(
        request,
        "networkpolicy_config.html",
        {
            "networkpolicy_form": networkpolicy_form,
            "rule_formset": rule_formset,
        },
    )


def explain_yaml_view(request):
    if request.method == "POST":
        yaml_output = request.POST.get("yaml_generated", "")
        selected_model = request.POST.get("selected_model", "")

        payload = {"yaml": yaml_output, "model": selected_model}

        explanation_response = requests.post(
            "http://yaml-explainer:8080/explain", json=payload
        )

        if explanation_response.status_code == 200:
            explanation = explanation_response.json().get(
                "explanation", "Sin explicación disponible."
            )
        elif explanation_response.status_code == 429:
            explanation = "⚠️ Modelo no disponible actualmente. Por favor, inténtelo de nuevo más tarde."
        elif explanation_response.status_code == 402:
            explanation = (
                "💳 Créditos insuficientes. "
                "Puedes añadir más en <a href='https://openrouter.ai/settings/credits' target='_blank'>OpenRouter</a> "
                "o utilizar un modelo gratuito."
            )
        else:
            explanation = (
                f"❌ Error al obtener explicación: {explanation_response.status_code}"
            )

        models, default_model = get_model_options()
        return render(
            request,
            "yaml_result.html",
            {
                "yaml_output": yaml_output,
                "explanation": explanation,
                "models": models,
                "selected_model": selected_model,
                "default_model": default_model,
            },
        )
    else:
        return redirect("configure_deployment")


def apply_yaml(request):
    if request.method == "POST":
        yaml_text = request.POST.get("yaml_generated", "")
        try:
            response = requests.post(
                "http://kube-manager:8080/deploy",
                data=yaml_text.encode("utf-8"),
                headers={"Content-Type": "application/x-yaml"},
                timeout=10,
            )
            if response.status_code == 200:
                messages.success(
                    request, "✅ YAML desplegado exitosamente en Kubernetes."
                )
            else:
                messages.error(request, f"❌ Error al aplicar YAML: {response.text}")
        except Exception as e:
            messages.error(request, f"❌ Fallo al conectarse al microservicio: {e}")
    models, default_model = get_model_options()
    return render(
        request,
        "yaml_result.html",
        {
            "yaml_output": yaml_text,
            "explanation": None,
            "models": models,
            "default_model": default_model,
        },
    )


def explore_resources(request):
    resource = request.GET.get("resource")
    if not resource:
        return HttpResponseBadRequest("Falta el parámetro 'resource'.")

    try:
        response = requests.get(
            "http://kube-manager:8080/list", params={"resource": resource}
        )
        response.raise_for_status()
        names = response.json()
    except Exception as e:
        return render(
            request,
            "explore.html",
            {
                "resource": resource,
                "error": f"Error consultando recursos: {str(e)}",
                "names": [],
            },
        )

    return render(
        request, "explore.html", {"resource": resource, "names": names, "error": None}
    )


@csrf_exempt
def delete_resource(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Solo se permite POST")

    resource = request.POST.get("resource")
    name = request.POST.get("name")

    try:
        requests.delete(
            "http://kube-manager:8080/resource",
            params={
                "type": resource,
                "name": name,
                "namespace": "default",
            },
        )
    except Exception as e:
        print(f"Error eliminando: {e}")

    return redirect(f"/explore/?resource={resource}")


def redirect_to_configure(request):
    return redirect("object_selector")


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
