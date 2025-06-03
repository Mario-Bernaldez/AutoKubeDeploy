# pylint: disable
# flake8: noqa

from app import utils
from django import forms
from django.forms import BaseFormSet, ValidationError, formset_factory
from .widgets import (
    HelpButtonCheckboxInput,
    HelpButtonCheckboxSelectMultiple,
    HelpButtonNumberInput,
    HelpButtonSelect,
    HelpButtonTextInput,
    HelpButtonTextarea,
)
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# --- Auxiliary form for service ports ---


class ServicePortForm(forms.Form):
    PROTOCOL_CHOICES = [
        ("TCP", "TCP"),
        ("UDP", "UDP"),
        ("SCTP", "SCTP"),
    ]

    port = forms.IntegerField(
        label=_("Port"),
        min_value=1,
        max_value=65535,
        widget=HelpButtonNumberInput(
            attrs={"required": True, "id": "id_port"},
            help_text=_("Port exposed by the Service (e.g. 80)."),
        ),
    )

    target_port = forms.IntegerField(
        label=_("Target Port"),
        min_value=1,
        max_value=65535,
        widget=HelpButtonNumberInput(
            attrs={"required": True, "id": "id_target_port"},
            help_text=_("Port on the target container (e.g. 8080)."),
        ),
    )

    protocol = forms.ChoiceField(
        label=_("Protocol"),
        choices=PROTOCOL_CHOICES,
        widget=HelpButtonSelect(
            attrs={"id": "id_protocol"},
            help_text=_("Network protocol used by this port."),
        ),
    )

    node_port = forms.IntegerField(
        label=_("Node Port"),
        min_value=30000,
        max_value=32767,
        required=False,
        widget=HelpButtonNumberInput(
            attrs={"class": "node-port-field", "id": "id_node_port"},
            help_text=_(
                "Optional: External port to expose if Service type is NodePort."
            ),
        ),
    )


ServicePortFormSet = formset_factory(ServicePortForm, extra=1)

# --- Main forms ---


class ObjectTypeForm(forms.Form):
    object_type = forms.ChoiceField(
        label="Select Object Type",
        choices=[
            ("deployment", "Deployment"),
            ("namespace", "Namespace"),
            ("service", "Service"),
            ("hpa", "Horizontal Pod Autoscaler"),
            ("configMap", "ConfigMap"),
            ("secret", "Secret"),
            ("pvc", "Persistent Volume Claim"),
            ("ingress", "Ingress"),
            ("sa", "Service Account"),
            ("rbac", "RBAC"),
            ("networkpolicy", "Network Policy"),
        ],
        widget=forms.RadioSelect,
    )


class DeploymentForm(forms.Form):
    name = forms.CharField(
        label=_("Deployment Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_deployment_name"},
            help_text=_("Name of the Deployment to be created."),
        ),
    )

    namespace = forms.CharField(
        label=_("Namespace"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_deployment_namespace"},
            help_text=_("Namespace for the deployment. Defaults to 'default'."),
        ),
    )

    replicas = forms.IntegerField(
        label=_("Replicas"),
        min_value=1,
        initial=1,
        widget=HelpButtonNumberInput(
            attrs={"id": "id_replicas"},
            help_text=_("Number of pod replicas to maintain."),
        ),
    )

    STRATEGY_CHOICES = [
        ("RollingUpdate", _("Rolling Update")),
        ("Recreate", _("Recreate")),
    ]
    strategy = forms.ChoiceField(
        label=_("Deployment Strategy"),
        choices=STRATEGY_CHOICES,
        widget=HelpButtonSelect(
            attrs={"id": "id_strategy"},
            help_text=_("Choose how updates are rolled out."),
        ),
    )

    max_unavailable = forms.CharField(
        label=_("Max Unavailable (RollingUpdate)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_max_unavailable",
                "pattern": r"^\d+%?$",
                "title": _("Must be an integer or percentage (e.g. 1 or 25%)"),
            },
            help_text=_(
                "Max number of pods that can be unavailable during the update."
            ),
        ),
        validators=[utils.validate_int_or_percent],
        initial="1",
    )

    max_surge = forms.CharField(
        label=_("Max Surge (RollingUpdate)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_max_surge",
                "pattern": r"^\d+%?$",
                "title": _("Must be an integer or percentage (e.g. 1 or 25%)"),
            },
            help_text=_("Max number of extra pods to create during the update."),
        ),
        validators=[utils.validate_int_or_percent],
        initial="1",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class PodTemplateForm(forms.Form):
    pod_name = forms.CharField(
        label=_("Pod Name"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_pod_name"},
            help_text=_("Optional name for the pod template."),
        ),
    )

    labels = forms.CharField(
        label=_("Pod Labels (key=value, comma-separated)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_pod_labels",
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": _("Must follow the format key=value, comma-separated."),
            },
            help_text=_(
                "Define labels to assign to the pod. Format: key=value,key2=value2"
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class ContainerForm(forms.Form):
    init_container = forms.BooleanField(
        label=_("Is Init Container?"),
        required=False,
        widget=HelpButtonCheckboxInput(
            attrs={"id": "id_init_container"},
            help_text=_(
                "Check this if the container should run before regular containers."
            ),
        ),
    )

    container_name = forms.CharField(
        label=_("Container Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_container_name"},
            help_text=_("Name of the container."),
        ),
    )

    image = forms.CharField(
        label=_("Container Image"),
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_image"},
            help_text=_("Container image name, e.g. nginx:latest."),
        ),
    )

    IMAGE_PULL_POLICY_CHOICES = [
        ("Always", _("Always")),
        ("IfNotPresent", _("If Not Present")),
        ("Never", _("Never")),
    ]
    image_pull_policy = forms.ChoiceField(
        label=_("Image Pull Policy"),
        choices=IMAGE_PULL_POLICY_CHOICES,
        widget=HelpButtonSelect(
            attrs={"id": "id_image_pull_policy"},
            help_text=_("Specify when to pull the image from the registry."),
        ),
    )

    command = forms.CharField(
        label=_("Command (space-separated)"),
        required=False,
        help_text=_("Example: /bin/sh -c 'echo hello'"),
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_command",
                "pattern": r"^[^\s]+(\s+[^\s]+)*$",
                "title": _(
                    "Should be a space-separated list, e.g. /bin/sh -c 'echo hello'"
                ),
            },
            help_text=_(
                "Command to execute in the container. Format: space-separated tokens."
            ),
        ),
    )

    ports = forms.CharField(
        label=_("Ports (comma-separated numbers)"),
        required=False,
        validators=[utils.validate_ports],
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_ports",
                "pattern": r"^(\d{1,5})(,\d{1,5})*$",
            },
            help_text=_("Container ports exposed, e.g. 80,443"),
        ),
    )

    env_vars = forms.CharField(
        label=_("Environment Variables (key=value, comma-separated)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_env_vars",
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": _("Must follow the format key=value, comma-separated."),
            },
            help_text=_(
                "Define environment variables for the container. Format: key=value,key2=value2"
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class VolumeMountForm(forms.Form):
    volume_name = forms.CharField(
        label=_("Volume Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"id": "id_volume_mount_name"},
            help_text=_("Name of the volume to mount."),
        ),
    )

    mount_path = forms.CharField(
        label=_("Mount Path"),
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={"id": "id_mount_path"},
            help_text=_(
                "Filesystem path inside the container where the volume will be mounted."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class VolumeForm(forms.Form):
    volume_name = forms.CharField(
        label=_("Volume Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"id": "id_volume_name"},
            help_text=_("Unique name for the volume within the pod specification."),
        ),
    )

    volume_type = forms.ChoiceField(
        label=_("Volume Type"),
        choices=[
            ("emptyDir", _("emptyDir")),
            ("hostPath", _("hostPath")),
            ("configMap", _("configMap")),
            ("secret", _("Secret")),
            ("persistentVolumeClaim", _("PersistentVolumeClaim")),
        ],
        widget=HelpButtonSelect(
            attrs={"id": "id_volume_type"},
            help_text=_("Select the type of volume to mount into the pod."),
        ),
    )

    medium = forms.CharField(
        label=_("Medium (for emptyDir)"),
        required=False,
        validators=[utils.validate_medium],
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_medium",
                "pattern": r"^$|^Memory$",
                "title": _("Leave empty or enter 'Memory' (case-sensitive)."),
            },
            help_text=_(
                "Enter 'Memory' to use memory-backed storage or leave blank for disk-backed."
            ),
        ),
    )

    size_limit = forms.CharField(
        label=_("Size Limit (for emptyDir)"),
        required=False,
        validators=[utils.validate_size_limit],
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_size_limit",
                "pattern": r"^\d+(Ki|Mi|Gi|Ti|Pi|Ei)$",
                "title": _("Example: 1Gi, 500Mi, 100Ki, etc."),
            },
            help_text=_("Optional limit for volume size (e.g., 1Gi, 500Mi)."),
        ),
    )

    path = forms.CharField(
        label=_("Path (for hostPath)"),
        required=False,
        validators=[utils.validate_absolute_path],
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_path",
                "pattern": r"^/.*",
                "title": _("Must be an absolute path, e.g. /data/volume"),
            },
            help_text=_(
                "Absolute path on the host machine to mount inside the container."
            ),
        ),
    )

    HOSTPATH_TYPE_CHOICES = [
        ("", _("— (empty) —")),
        ("Directory", _("Directory")),
        ("DirectoryOrCreate", _("DirectoryOrCreate")),
        ("File", _("File")),
        ("FileOrCreate", _("FileOrCreate")),
        ("Socket", _("Socket")),
        ("CharDevice", _("CharDevice")),
        ("BlockDevice", _("BlockDevice")),
    ]

    hostpath_type = forms.ChoiceField(
        label=_("HostPath Type (for hostPath)"),
        required=False,
        choices=HOSTPATH_TYPE_CHOICES,
        widget=HelpButtonSelect(
            attrs={"id": "id_hostpath_type"},
            help_text=_(
                "Specify the type of the host path if required (e.g., File, Directory)."
            ),
        ),
    )

    config_map_name = forms.CharField(
        label=_("ConfigMap Name (for configMap)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_config_map_name"},
            help_text=_("Name of the ConfigMap resource to mount as a volume."),
        ),
    )

    secret_name = forms.CharField(
        label=_("Secret Name (for Secret)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_secret_name"},
            help_text=_("Name of the Secret to mount as a volume."),
        ),
    )

    pvc_claim_name = forms.CharField(
        label=_("PVC Claim Name (for PersistentVolumeClaim)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_pvc_claim_name"},
            help_text=_("Name of the PersistentVolumeClaim to bind to this volume."),
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        vtype = cleaned_data.get("volume_type")

        if vtype == "hostPath" and not cleaned_data.get("path"):
            self.add_error("path", _("This field is required for hostPath."))

        if vtype == "configMap" and not cleaned_data.get("config_map_name"):
            self.add_error(
                "config_map_name", _("This field is required for configMap.")
            )

        if vtype == "secret" and not cleaned_data.get("secret_name"):
            self.add_error("secret_name", _("This field is required for Secret."))

        if vtype == "persistentVolumeClaim" and not cleaned_data.get("pvc_claim_name"):
            self.add_error(
                "pvc_claim_name", _("This field is required for PersistentVolumeClaim.")
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class NamespaceForm(forms.Form):
    namespace_name = forms.CharField(
        label=_("Namespace Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={
                "placeholder": "e.g. production",
                "id": "id_namespace_name",
            },
            help_text=_(
                "The name of the namespace. This will be used to logically separate resources in your cluster."
            ),
        ),
    )

    labels = forms.CharField(
        label=_("Namespace Labels"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "placeholder": "env=prod, team=devops",
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": _("Must follow the format key=value, comma-separated."),
                "id": "id_labels",
            },
            help_text=_(
                "Optional key=value pairs used to organize and select resources. Default: empty."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class ServiceForm(forms.Form):
    service_name = forms.CharField(
        label=_("Service Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"id": "id_service_name"},
            help_text=_("Name of the Service resource."),
        ),
    )

    namespace = forms.CharField(
        label=_("Namespace"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_service_namespace"},
            help_text=_("Namespace for the Service. Defaults to 'default'."),
        ),
    )

    service_type = forms.ChoiceField(
        label=_("Service Type"),
        choices=[
            ("ClusterIP", _("ClusterIP")),
            ("NodePort", _("NodePort")),
            ("LoadBalancer", _("LoadBalancer")),
        ],
        widget=HelpButtonSelect(
            attrs={"id": "id_service_type"},
            help_text=_(
                "Select how the Service is exposed: internal, via node ports, or load balancer."
            ),
        ),
    )

    selector = forms.CharField(
        label=_("Service Selector (key=value, comma-separated)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_service_selector",
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": _("Must follow the format key=value, comma-separated."),
            },
            help_text=_(
                "Label selector to match the target pods. Format: app=frontend,role=api"
            ),
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class HPAForm(forms.Form):
    hpa_name = forms.CharField(
        label=_("HPA Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_hpa_name"},
            help_text=_("Name of the HorizontalPodAutoscaler resource."),
        ),
    )

    namespace = forms.CharField(
        label=_("Namespace"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default", "id": "id_hpa_namespace"},
            help_text=_(
                "Namespace where the HPA will be created. Defaults to 'default'."
            ),
        ),
    )

    target_deployment = forms.CharField(
        label=_("Target Deployment Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_target_deployment"},
            help_text=_("The name of the Deployment the HPA will scale."),
        ),
    )

    min_replicas = forms.IntegerField(
        label=_("Minimum Replicas"),
        min_value=1,
        initial=1,
        widget=HelpButtonNumberInput(
            attrs={"required": True, "id": "id_min_replicas"},
            help_text=_("Minimum number of pod replicas allowed."),
        ),
    )

    max_replicas = forms.IntegerField(
        label=_("Maximum Replicas"),
        min_value=1,
        initial=1,
        widget=HelpButtonNumberInput(
            attrs={"required": True, "id": "id_max_replicas"},
            help_text=_("Maximum number of pod replicas allowed."),
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        min_replicas = cleaned_data.get("min_replicas")
        max_replicas = cleaned_data.get("max_replicas")

        if min_replicas is not None and max_replicas is not None:
            if min_replicas > max_replicas:
                raise forms.ValidationError(
                    _("Minimum Replicas cannot be greater than Maximum Replicas.")
                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class HPAMetricForm(forms.Form):
    resource_name = forms.ChoiceField(
        label=_("Resource Name"),
        choices=[
            ("cpu", _("CPU")),
            ("memory", _("Memory")),
        ],
        widget=HelpButtonSelect(
            attrs={"id": "id_resource_name"},
            help_text=_("The resource type to scale by: CPU or Memory."),
        ),
    )

    target_type = forms.ChoiceField(
        label=_("Target Type"),
        choices=[
            ("Utilization", _("Utilization (%)")),
            ("Value", _("Value (absolute)")),
        ],
        widget=HelpButtonSelect(
            attrs={"id": "id_target_type"},
            help_text=_(
                "Choose whether to scale based on percentage utilization or an absolute value."
            ),
        ),
    )

    target_value = forms.IntegerField(
        label=_("Target Value"),
        min_value=1,
        widget=HelpButtonNumberInput(
            attrs={"required": True, "id": "id_target_value"},
            help_text=_(
                "Use a percentage (e.g. 80) for utilization or an absolute unit (e.g. 500Mi) for value."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class ConfigMapForm(forms.Form):
    configmap_name = forms.CharField(
        label=_("ConfigMap Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_configmap_name"},
            help_text=_(
                "The name of the ConfigMap object that will store key-value configuration data."
            ),
        ),
    )

    namespace = forms.CharField(
        label=_("Namespace"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default", "id": "id_namespace"},
            help_text=_(
                "The namespace where the ConfigMap will be created. Defaults to 'default' if left blank."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class ConfigMapKeyForm(forms.Form):
    key_name = forms.CharField(
        label=_("Key"),
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_key_name"},
            help_text=_(
                "The key under which the value will be stored in the ConfigMap. Must be unique within the ConfigMap."
            ),
        ),
    )

    is_multiline = forms.BooleanField(
        label=_("Multiline content (like file data)?"),
        required=False,
        initial=False,
        widget=HelpButtonCheckboxInput(
            attrs={"id": "id_is_multiline"},
            help_text=_(
                "Check this box if the value is multiline, such as file content or scripts."
            ),
        ),
    )

    value = forms.CharField(
        label=_("Value"),
        widget=HelpButtonTextarea(
            attrs={"rows": 3, "required": True, "id": "id_value"},
            help_text=_(
                "The content to store for this key. If multiline, use \\n or enable the checkbox above."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class SecretForm(forms.Form):
    secret_name = forms.CharField(
        label=_("Secret Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_secret_name"},
            help_text=_(
                "Name of the Secret resource. Must be unique within the namespace."
            ),
        ),
    )

    namespace = forms.CharField(
        label=_("Namespace"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default", "id": "id_secret_namespace"},
            help_text=_(
                "Namespace to store the secret. Defaults to 'default' if left blank."
            ),
        ),
    )

    secret_type = forms.ChoiceField(
        label=_("Secret Type"),
        choices=[
            ("Opaque", _("Opaque (key-value)")),
            ("kubernetes.io/tls", _("TLS (Certificate and Private Key)")),
            (
                "kubernetes.io/dockerconfigjson",
                _("Docker Config JSON (.dockerconfigjson)"),
            ),
        ],
        widget=HelpButtonSelect(
            attrs={"id": "id_secret_type"},
            help_text=_(
                "Select the type of secret depending on its purpose: generic data, TLS certs, or Docker credentials."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class OpaqueKeyForm(forms.Form):
    key_name = forms.CharField(
        label=_("Key"),
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_opaque_key_name"},
            help_text=_("The key under which the value will be stored in the secret."),
        ),
    )

    value = forms.CharField(
        label=_("Value"),
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_opaque_value"},
            help_text=_("The value corresponding to the specified key."),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class TLSSecretForm(forms.Form):
    tls_crt = forms.CharField(
        label=_("TLS Certificate (tls.crt)"),
        widget=HelpButtonTextarea(
            attrs={"rows": 4, "required": True, "id": "id_tls_crt"},
            help_text=_(
                "Paste the full TLS certificate content (usually starts with -----BEGIN CERTIFICATE-----)."
            ),
        ),
    )

    tls_key = forms.CharField(
        label=_("TLS Private Key (tls.key)"),
        widget=HelpButtonTextarea(
            attrs={"rows": 4, "required": True, "id": "id_tls_key"},
            help_text=_("Paste the associated private key for the TLS certificate."),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class DockerConfigJSONForm(forms.Form):
    dockerconfigjson = forms.CharField(
        label=_("Docker Config JSON (.dockerconfigjson)"),
        widget=HelpButtonTextarea(
            attrs={"rows": 8, "required": True, "id": "id_dockerconfigjson"},
            help_text=_(
                "Paste the entire content of the Docker config JSON used to authenticate with private registries."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class PersistentVolumeClaimForm(forms.Form):
    pvc_name = forms.CharField(
        label=_("PVC Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_pvc_name"},
            help_text=_(
                "Name of the PersistentVolumeClaim. Must be unique within the namespace."
            ),
        ),
    )

    namespace = forms.CharField(
        label=_("Namespace"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default", "id": "id_pvc_namespace"},
            help_text=_(
                "Namespace where the PVC will be created. Defaults to 'default' if left blank."
            ),
        ),
    )

    storage_request = forms.CharField(
        label=_("Requested Storage (e.g., 1Gi, 500Mi)"),
        max_length=20,
        widget=HelpButtonTextInput(
            attrs={
                "required": True,
                "pattern": r"^\d+(Ki|Mi|Gi|Ti|Pi|Ei)$",
                "title": _("Must be a valid size like 1Gi, 500Mi, 100Ki, etc."),
                "id": "id_storage_request",
            },
            help_text=_(
                "Amount of storage to request. Use units like Mi, Gi, Ti, etc."
            ),
        ),
    )

    access_modes = forms.MultipleChoiceField(
        label=_("Access Modes"),
        choices=[
            ("ReadWriteOnce", _("ReadWriteOnce")),
            ("ReadOnlyMany", _("ReadOnlyMany")),
            ("ReadWriteMany", _("ReadWriteMany")),
        ],
        widget=HelpButtonCheckboxSelectMultiple(
            attrs={"id": "id_access_modes"},
            help_text=_(
                "Select one or more access modes. 'ReadWriteOnce' is the most common."
            ),
        ),
    )

    storage_class_name = forms.CharField(
        label=_("Storage Class Name (Optional)"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "placeholder": _("Leave empty for default"),
                "id": "id_storage_class_name",
            },
            help_text=_(
                "Name of the storage class to use. Leave empty to use the cluster's default class."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class IngressForm(forms.Form):
    ingress_name = forms.CharField(
        label=_("Ingress Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_ingress_name"},
            help_text=_("Name of the Ingress resource to be created."),
        ),
    )

    namespace = forms.CharField(
        label=_("Namespace"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default", "id": "id_ingress_namespace"},
            help_text=_("Namespace for the Ingress. Defaults to 'default'."),
        ),
    )

    host = forms.CharField(
        label=_("Host"),
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={
                "required": True,
                "placeholder": _("example.com"),
                "pattern": r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$",
                "title": _("Must be a valid domain, e.g., example.com"),
                "id": "id_ingress_host",
            },
            help_text=_(
                "Fully qualified domain name for routing. Example: app.example.com"
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class IngressPathForm(forms.Form):
    path = forms.CharField(
        label=_("Path"),
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={"required": True, "placeholder": "/", "id": "id_path"},
            help_text=_("URL path to route traffic to the service. Example: / or /api"),
        ),
    )

    service_name = forms.CharField(
        label=_("Service Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_service_name"},
            help_text=_("The name of the Kubernetes Service to forward traffic to."),
        ),
    )

    service_port = forms.IntegerField(
        label=_("Service Port"),
        min_value=1,
        max_value=65535,
        widget=HelpButtonNumberInput(
            attrs={"required": True, "id": "id_service_port"},
            help_text=_("Port number on which the target Service is listening."),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class ServiceAccountForm(forms.Form):
    service_account_name = forms.CharField(
        label=_("ServiceAccount Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text=_(
                "The name of the ServiceAccount resource to be created or referenced."
            ),
        ),
    )

    namespace = forms.CharField(
        label=_("Namespace"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default"},
            help_text=_(
                "The namespace where the ServiceAccount resides. If omitted, 'default' will be used."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class ImagePullSecretForm(forms.Form):
    secret_name = forms.CharField(
        label=_("Image Pull Secret Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text=_(
                "The name of the Kubernetes secret used to authenticate when pulling images from a private registry."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class RoleForm(forms.Form):
    role_type = forms.ChoiceField(
        label=_("Role Type"),
        choices=[
            ("Role", _("Role (namespaced)")),
            ("ClusterRole", _("ClusterRole (cluster-wide)")),
        ],
        widget=HelpButtonSelect(
            attrs={"id": "id_role_type"},
            help_text=_(
                "Select 'Role' to apply permissions within a namespace or 'ClusterRole' for cluster-wide access."
            ),
        ),
    )

    role_name = forms.CharField(
        label=_("Role/ClusterRole Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text=_("The name of the Role or ClusterRole to create or bind to."),
        ),
    )

    namespace = forms.CharField(
        label=_("Namespace (only for Role)"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_namespace_name",
                "placeholder": _("Leave empty for ClusterRole"),
            },
            help_text=_(
                "Required only when creating a Role. Leave empty for ClusterRoles."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class RuleForm(forms.Form):
    api_groups = forms.CharField(
        label=_("API Groups (comma-separated, empty for core)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": ""},
            help_text=_(
                "Comma-separated list of API groups this rule applies to. Leave empty for the core API group."
            ),
        ),
    )

    resources = forms.CharField(
        label=_("Resources (comma-separated)"),
        required=True,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text=_(
                "List of resource types (e.g., pods, services) this rule applies to."
            ),
        ),
    )

    verbs = forms.CharField(
        label=_("Verbs (comma-separated)"),
        required=True,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text=_(
                "Actions allowed: e.g., get, list, watch, create, delete, update."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class RoleBindingForm(forms.Form):
    binding_name = forms.CharField(
        label=_("Binding Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text=_("The name of the RoleBinding or ClusterRoleBinding."),
        ),
    )

    namespace_binding = forms.CharField(
        label=_("Namespace (only for RoleBinding)"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_binding_namespace",
                "placeholder": _("Leave empty for ClusterRoleBinding"),
            },
            help_text=_("Specify the namespace only if creating a RoleBinding."),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class SubjectForm(forms.Form):
    kind = forms.ChoiceField(
        label=_("Subject Kind"),
        choices=[
            ("User", _("User")),
            ("Group", _("Group")),
            ("ServiceAccount", _("ServiceAccount")),
        ],
        widget=HelpButtonSelect(
            help_text=_(
                "Select the type of subject to bind: a User, a Group, or a ServiceAccount."
            ),
        ),
    )

    name = forms.CharField(
        label=_("Subject Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text=_(
                "The name of the user, group, or service account to grant access to."
            ),
        ),
    )

    namespace = forms.CharField(
        label=_("Subject Namespace (only for ServiceAccount)"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": _("Only required for ServiceAccount")},
            help_text=_(
                "Required only if the subject is a ServiceAccount. Leave empty otherwise."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class NetworkPolicyForm(forms.Form):
    name = forms.CharField(
        label=_("NetworkPolicy Name"),
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text=_(
                "The name of the NetworkPolicy resource. It must be unique within the namespace."
            ),
        ),
    )

    namespace = forms.CharField(
        label=_("Namespace"),
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"required": False},
            help_text=_(
                "The namespace to which this NetworkPolicy will apply. Defaults to 'default' if left blank."
            ),
        ),
    )

    pod_selector = forms.CharField(
        label=_("Pod Selector (key=value, comma-separated)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "placeholder": _("app=frontend,role=api"),
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": _("Format: key=value, separated by commas"),
            },
            help_text=_(
                "Selects the pods to which this policy applies. Format: key=value pairs separated by commas."
            ),
        ),
    )

    policy_types = forms.MultipleChoiceField(
        label=_("Policy Types"),
        choices=[("Ingress", _("Ingress")), ("Egress", _("Egress"))],
        widget=HelpButtonCheckboxSelectMultiple(
            help_text=_(
                "Choose one or both to specify the traffic direction: 'Ingress' for incoming or 'Egress' for outgoing."
            ),
        ),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class NetworkRuleForm(forms.Form):
    direction = forms.ChoiceField(
        label=_("Direction"),
        choices=[("Ingress", _("Ingress")), ("Egress", _("Egress"))],
        widget=HelpButtonSelect(
            attrs={"class": "direction-select"},
            help_text=_(
                "Defines the direction of traffic this rule applies to: Ingress (incoming) or Egress (outgoing)."
            ),
        ),
    )

    ports = forms.CharField(
        label=_("Ports (comma-separated)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={"pattern": r"^(\d{1,5})(,\d{1,5})*$"},
            help_text=_(
                "List of ports to allow or restrict, separated by commas. Example: 80,443,8080"
            ),
        ),
    )

    pod_selector = forms.CharField(
        label=_("Pod Selector (key=value, comma-separated)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": _("role=db")},
            help_text=_(
                "Applies the rule to traffic from/to pods matching these labels. Format: key=value"
            ),
        ),
    )

    namespace_selector = forms.CharField(
        label=_("Namespace Selector (key=value, comma-separated)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": _("env=prod")},
            help_text=_(
                "Restrict the rule to namespaces matching these labels. Format: key=value"
            ),
        ),
    )

    ip_block = forms.CharField(
        label=_("IP Block (CIDR)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": _("192.168.1.0/24")},
            help_text=_("Specify a CIDR range to apply the rule to a set of IPs."),
        ),
    )

    except_ips = forms.CharField(
        label=_("IP Exceptions (comma-separated CIDRs)"),
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": _("192.168.1.5/32,192.168.1.6/32")},
            help_text=_(
                "List of CIDR IPs to exclude from the IP block. Separate multiple entries with commas."
            ),
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(
                    f"{field.label} <span style='color: black;'>* </span>"
                )


class RequiredContainerFormSet(BaseFormSet):
    def clean(self):
        """
        Ensures that at least one container form is filled out and valid.
        """
        super().clean()

        if any(self.errors):
            # If there are already errors in individual forms, skip further validation
            return

        has_data = False
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                has_data = True
                break

        if not has_data:
            raise ValidationError(_("You must add at least one container."))
