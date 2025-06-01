# pylint: disable
# flake8: noqa

from app import utils
from django import forms
from django.forms import BaseFormSet, ValidationError, formset_factory
from .widgets import HelpButtonTextInput
from django.utils.safestring import mark_safe
# --- Auxiliary form for service ports ---


class ServicePortForm(forms.Form):
    PROTOCOL_CHOICES = [
        ("TCP", "TCP"),
        ("UDP", "UDP"),
        ("SCTP", "SCTP"),
    ]

    port = forms.IntegerField(
        label="Port",
        min_value=1,
        max_value=65535,
        widget=forms.NumberInput(attrs={"required": True, "id": "id_port"}),
        help_text="Port exposed by the Service (e.g. 80)."
    )

    target_port = forms.IntegerField(
        label="Target Port",
        min_value=1,
        max_value=65535,
        widget=forms.NumberInput(attrs={"required": True, "id": "id_target_port"}),
        help_text="Port on the target container (e.g. 8080)."
    )

    protocol = forms.ChoiceField(
        label="Protocol",
        choices=PROTOCOL_CHOICES,
        widget=forms.Select(attrs={"id": "id_protocol"}),
        help_text="Network protocol used by this port."
    )

    node_port = forms.IntegerField(
        label="Node Port (only for NodePort)",
        min_value=30000,
        max_value=32767,
        required=False,
        widget=forms.NumberInput(attrs={"class": "node-port-field", "id": "id_node_port"}),
        help_text="Optional: External port to expose if Service type is NodePort."
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
        label="Deployment Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_deployment_name"},
            help_text="Name of the Deployment to be created."
        ),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_deployment_namespace"},
            help_text="Namespace for the deployment. Defaults to 'default'."
        ),
    )

    replicas = forms.IntegerField(
        label="Replicas",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={"id": "id_replicas"}),
        help_text="Number of pod replicas to maintain."
    )

    STRATEGY_CHOICES = [("RollingUpdate", "Rolling Update"), ("Recreate", "Recreate")]
    strategy = forms.ChoiceField(
        label="Deployment Strategy",
        choices=STRATEGY_CHOICES,
        widget=forms.Select(attrs={"id": "id_strategy"}),
        help_text="Choose how updates are rolled out."
    )

    max_unavailable = forms.CharField(
        label="Max Unavailable (RollingUpdate)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_max_unavailable",
                "pattern": r"^\d+%?$",
                "title": "Must be an integer or percentage (e.g. 1 or 25%)",
            },
            help_text="Max number of pods that can be unavailable during the update."
        ),
        validators=[utils.validate_int_or_percent],
        initial="1",
    )

    max_surge = forms.CharField(
        label="Max Surge (RollingUpdate)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_max_surge",
                "pattern": r"^\d+%?$",
                "title": "Must be an integer or percentage (e.g. 1 or 25%)",
            },
            help_text="Max number of extra pods to create during the update."
        ),
        validators=[utils.validate_int_or_percent],
        initial="1",
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class PodTemplateForm(forms.Form):
    pod_name = forms.CharField(
        label="Pod Name",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_pod_name"},
            help_text="Optional name for the pod template."
        ),
    )

    labels = forms.CharField(
        label="Pod Labels (key=value, comma-separated)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_pod_labels",
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": "Must follow the format key=value, comma-separated.",
            },
            help_text="Define labels to assign to the pod. Format: key=value,key2=value2"
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class ContainerForm(forms.Form):
    init_container = forms.BooleanField(
        label="Is Init Container?",
        required=False,
        widget=forms.CheckboxInput(attrs={"id": "id_init_container"}),
        help_text="Check this if the container should run before regular containers."
    )

    container_name = forms.CharField(
        label="Container Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_container_name"},
            help_text="Name of the container."
        ),
    )

    image = forms.CharField(
        label="Container Image",
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_image"},
            help_text="Container image name, e.g. nginx:latest."
        ),
    )

    IMAGE_PULL_POLICY_CHOICES = [
        ("Always", "Always"),
        ("IfNotPresent", "If Not Present"),
        ("Never", "Never"),
    ]
    image_pull_policy = forms.ChoiceField(
        label="Image Pull Policy",
        choices=IMAGE_PULL_POLICY_CHOICES,
        widget=forms.Select(attrs={"id": "id_image_pull_policy"}),
        help_text="Specify when to pull the image from the registry."
    )

    command = forms.CharField(
        label="Command (space-separated)",
        required=False,
        help_text="Example: /bin/sh -c 'echo hello'",
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_command",
                "pattern": r"^[^\s]+(\s+[^\s]+)*$",
                "title": "Should be a space-separated list, e.g. /bin/sh -c 'echo hello'",
            },
            help_text="Command to execute in the container. Format: space-separated tokens."
        ),
    )

    ports = forms.CharField(
        label="Ports (comma-separated numbers)",
        required=False,
        validators=[utils.validate_ports],
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_ports",
                "pattern": r"^(\d{1,5})(,\d{1,5})*$",
            },
            help_text="Container ports exposed, e.g. 80,443"
        ),
    )

    env_vars = forms.CharField(
        label="Environment Variables (key=value, comma-separated)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_env_vars",
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": "Must follow the format key=value, comma-separated.",
            },
            help_text="Define environment variables for the container. Format: key=value,key2=value2"
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class VolumeMountForm(forms.Form):
    volume_name = forms.CharField(
        label="Volume Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"id": "id_volume_mount_name"},
            help_text="Name of the volume to mount."
        ),
    )
    mount_path = forms.CharField(
        label="Mount Path",
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={"id": "id_mount_path"},
            help_text="Filesystem path inside the container where the volume will be mounted."
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class VolumeForm(forms.Form):
    volume_name = forms.CharField(
        label="Volume Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"id": "id_volume_name"},
            help_text="Unique name for the volume within the pod specification."
        ),
    )

    volume_type = forms.ChoiceField(
        label="Volume Type",
        choices=[
            ("emptyDir", "emptyDir"),
            ("hostPath", "hostPath"),
            ("configMap", "configMap"),
            ("secret", "Secret"),
            ("persistentVolumeClaim", "PersistentVolumeClaim"),
        ],
        widget=forms.Select(attrs={"id": "id_volume_type"}),
        help_text="Select the type of volume to mount into the pod."
    )

    # EmptyDir fields
    medium = forms.CharField(
        label="Medium (for emptyDir)",
        required=False,
        validators=[utils.validate_medium],
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_medium",
                "pattern": r"^$|^Memory$",
                "title": "Leave empty or enter 'Memory' (case-sensitive).",
            },
            help_text="Enter 'Memory' to use memory-backed storage or leave blank for disk-backed."
        ),
    )

    size_limit = forms.CharField(
        label="Size Limit (for emptyDir)",
        required=False,
        validators=[utils.validate_size_limit],
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_size_limit",
                "pattern": r"^\d+(Ki|Mi|Gi|Ti|Pi|Ei)$",
                "title": "Example: 1Gi, 500Mi, 100Ki, etc.",
            },
            help_text="Optional limit for volume size (e.g., 1Gi, 500Mi)."
        ),
    )

    # HostPath fields
    path = forms.CharField(
        label="Path (for hostPath)",
        required=False,
        validators=[utils.validate_absolute_path],
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_path",
                "pattern": r"^/.*",
                "title": "Must be an absolute path, e.g. /data/volume",
            },
            help_text="Absolute path on the host machine to mount inside the container."
        ),
    )

    HOSTPATH_TYPE_CHOICES = [
        ("", "— (empty) —"),
        ("Directory", "Directory"),
        ("DirectoryOrCreate", "DirectoryOrCreate"),
        ("File", "File"),
        ("FileOrCreate", "FileOrCreate"),
        ("Socket", "Socket"),
        ("CharDevice", "CharDevice"),
        ("BlockDevice", "BlockDevice"),
    ]

    hostpath_type = forms.ChoiceField(
        label="HostPath Type (for hostPath)",
        required=False,
        choices=HOSTPATH_TYPE_CHOICES,
        widget=forms.Select(attrs={"id": "id_hostpath_type"}),
        help_text="Specify the type of the host path if required (e.g., File, Directory)."
    )

    # ConfigMap
    config_map_name = forms.CharField(
        label="ConfigMap Name (for configMap)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_config_map_name"},
            help_text="Name of the ConfigMap resource to mount as a volume."
        ),
    )

    # Secret
    secret_name = forms.CharField(
        label="Secret Name (for Secret)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_secret_name"},
            help_text="Name of the Secret to mount as a volume."
        ),
    )

    # PVC
    pvc_claim_name = forms.CharField(
        label="PVC Claim Name (for PersistentVolumeClaim)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_pvc_claim_name"},
            help_text="Name of the PersistentVolumeClaim to bind to this volume."
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        vtype = cleaned_data.get("volume_type")

        if vtype == "hostPath" and not cleaned_data.get("path"):
            self.add_error("path", "This field is required for hostPath.")

        if vtype == "configMap" and not cleaned_data.get("config_map_name"):
            self.add_error("config_map_name", "This field is required for configMap.")

        if vtype == "secret" and not cleaned_data.get("secret_name"):
            self.add_error("secret_name", "This field is required for Secret.")

        if vtype == "persistentVolumeClaim" and not cleaned_data.get("pvc_claim_name"):
            self.add_error("pvc_claim_name", "This field is required for PersistentVolumeClaim.")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class NamespaceForm(forms.Form):
    namespace_name = forms.CharField(
        label="Namespace Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={
                "placeholder": "e.g. production",
                "id": "id_namespace_name"
            },
            help_text="The name of the namespace. This will be used to logically separate resources in your cluster."
        )
    )

    labels = forms.CharField(
        label="Namespace Labels",
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "placeholder": "env=prod, team=devops",
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": "Must follow the format key=value, comma-separated.",
                "id": "id_labels"
            },
            help_text="Optional key=value pairs used to organize and select resources. Default: empty."
        )
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")


class ServiceForm(forms.Form):
    service_name = forms.CharField(
        label="Service Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"id": "id_service_name"},
            help_text="Name of the Service resource."
        ),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_service_namespace"},
            help_text="Namespace for the Service. Defaults to 'default'."
        ),
    )

    service_type = forms.ChoiceField(
        label="Service Type",
        choices=[
            ("ClusterIP", "ClusterIP"),
            ("NodePort", "NodePort"),
            ("LoadBalancer", "LoadBalancer"),
        ],
        widget=forms.Select(attrs={"id": "id_service_type"}),
        help_text="Select how the Service is exposed: internal, via node ports, or load balancer."
    )

    selector = forms.CharField(
        label="Service Selector (key=value, comma-separated)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "id": "id_service_selector",
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": "Must follow the format key=value, comma-separated.",
            },
            help_text="Label selector to match the target pods. Format: app=frontend,role=api"
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")



class HPAForm(forms.Form):
    hpa_name = forms.CharField(
        label="HPA Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_hpa_name"},
            help_text="Name of the HorizontalPodAutoscaler resource."
        ),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default", "id": "id_hpa_namespace"},
            help_text="Namespace where the HPA will be created. Defaults to 'default'."
        ),
    )

    target_deployment = forms.CharField(
        label="Target Deployment Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_target_deployment"},
            help_text="The name of the Deployment the HPA will scale."
        ),
    )

    min_replicas = forms.IntegerField(
        label="Minimum Replicas",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={"required": True, "id": "id_min_replicas"}),
        help_text="Minimum number of pod replicas allowed."
    )

    max_replicas = forms.IntegerField(
        label="Maximum Replicas",
        min_value=1,
        widget=forms.NumberInput(attrs={"required": True, "id": "id_max_replicas"}),
        help_text="Maximum number of pod replicas allowed."
    )

    def clean(self):
        cleaned_data = super().clean()
        min_replicas = cleaned_data.get("min_replicas")
        max_replicas = cleaned_data.get("max_replicas")

        if min_replicas is not None and max_replicas is not None:
            if min_replicas > max_replicas:
                raise forms.ValidationError(
                    "Minimum Replicas cannot be greater than Maximum Replicas."
                )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")



class HPAMetricForm(forms.Form):
    resource_name = forms.ChoiceField(
        label="Resource Name",
        choices=[("cpu", "CPU"), ("memory", "Memory")],
        widget=forms.Select(attrs={"id": "id_resource_name"}),
        help_text="The resource type to scale by: CPU or Memory."
    )

    target_type = forms.ChoiceField(
        label="Target Type",
        choices=[("Utilization", "Utilization (%)"), ("Value", "Value (absolute)")],
        widget=forms.Select(attrs={"id": "id_target_type"}),
        help_text="Choose whether to scale based on percentage utilization or an absolute value."
    )

    target_value = forms.IntegerField(
        label="Target Value",
        min_value=1,
        widget=forms.NumberInput(attrs={"required": True, "id": "id_target_value"}),
        help_text="Use a percentage (e.g. 80) for utilization or an absolute unit (e.g. 500Mi) for value."
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")


class ConfigMapForm(forms.Form):
    configmap_name = forms.CharField(
        label="ConfigMap Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_configmap_name"},
            help_text="The name of the ConfigMap object that will store key-value configuration data."
        ),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default", "id": "id_namespace"},
            help_text="The namespace where the ConfigMap will be created. Defaults to 'default' if left blank."
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class ConfigMapKeyForm(forms.Form):
    key_name = forms.CharField(
        label="Key",
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_key_name"},
            help_text="The key under which the value will be stored in the ConfigMap. Must be unique within the ConfigMap."
        ),
    )

    is_multiline = forms.BooleanField(
        label="Multiline content (like file data)?",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={"id": "id_is_multiline"}),
        help_text="Check this box if the value is multiline, such as file content or scripts."
    )

    value = forms.CharField(
        label="Value",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "required": True,
                "id": "id_value"
            }
        ),
        help_text="The content to store for this key. If multiline, use \\n or enable the checkbox above."
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class SecretForm(forms.Form):
    secret_name = forms.CharField(
        label="Secret Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_secret_name"},
            help_text="Name of the Secret resource. Must be unique within the namespace."
        ),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default", "id": "id_secret_namespace"},
            help_text="Namespace to store the secret. Defaults to 'default' if left blank."
        ),
    )

    secret_type = forms.ChoiceField(
        label="Secret Type",
        choices=[
            ("Opaque", "Opaque (key-value)"),
            ("kubernetes.io/tls", "TLS (Certificate and Private Key)"),
            ("kubernetes.io/dockerconfigjson", "Docker Config JSON (.dockerconfigjson)"),
        ],
        widget=forms.Select(attrs={"id": "id_secret_type"}),
        help_text="Select the type of secret depending on its purpose: generic data, TLS certs, or Docker credentials."
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class OpaqueKeyForm(forms.Form):
    key_name = forms.CharField(
        label="Key",
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_opaque_key_name"},
            help_text="The key under which the value will be stored in the secret."
        ),
    )

    value = forms.CharField(
        label="Value",
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_opaque_value"},
            help_text="The value corresponding to the specified key."
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class TLSSecretForm(forms.Form):
    tls_crt = forms.CharField(
        label="TLS Certificate (tls.crt)",
        widget=forms.Textarea(
            attrs={"rows": 4, "required": True, "id": "id_tls_crt"}
        ),
        help_text="Paste the full TLS certificate content (usually starts with -----BEGIN CERTIFICATE-----)."
    )

    tls_key = forms.CharField(
        label="TLS Private Key (tls.key)",
        widget=forms.Textarea(
            attrs={"rows": 4, "required": True, "id": "id_tls_key"}
        ),
        help_text="Paste the associated private key for the TLS certificate."
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class DockerConfigJSONForm(forms.Form):
    dockerconfigjson = forms.CharField(
        label="Docker Config JSON (.dockerconfigjson)",
        widget=forms.Textarea(
            attrs={"rows": 8, "required": True, "id": "id_dockerconfigjson"}
        ),
        help_text="Paste the entire content of the Docker config JSON used to authenticate with private registries."
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class PersistentVolumeClaimForm(forms.Form):
    pvc_name = forms.CharField(
        label="PVC Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_pvc_name"},
            help_text="Name of the PersistentVolumeClaim. Must be unique within the namespace."
        ),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default", "id": "id_pvc_namespace"},
            help_text="Namespace where the PVC will be created. Defaults to 'default' if left blank."
        ),
    )

    storage_request = forms.CharField(
        label="Requested Storage (e.g., 1Gi, 500Mi)",
        max_length=20,
        widget=HelpButtonTextInput(
            attrs={
                "required": True,
                "pattern": r"^\d+(Ki|Mi|Gi|Ti|Pi|Ei)$",
                "title": "Must be a valid size like 1Gi, 500Mi, 100Ki, etc.",
                "id": "id_storage_request"
            },
            help_text="Amount of storage to request. Use units like Mi, Gi, Ti, etc."
        ),
    )

    access_modes = forms.MultipleChoiceField(
        label="Access Modes",
        choices=[
            ("ReadWriteOnce", "ReadWriteOnce"),
            ("ReadOnlyMany", "ReadOnlyMany"),
            ("ReadWriteMany", "ReadWriteMany"),
        ],
        widget=forms.CheckboxSelectMultiple(attrs={"id": "id_access_modes"}),
        help_text="Select one or more access modes. 'ReadWriteOnce' is the most common."
    )

    storage_class_name = forms.CharField(
        label="Storage Class Name (Optional)",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "Leave empty for default", "id": "id_storage_class_name"},
            help_text="Name of the storage class to use. Leave empty to use the cluster's default class."
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class IngressForm(forms.Form):
    ingress_name = forms.CharField(
        label="Ingress Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_ingress_name"},
            help_text="Name of the Ingress resource to be created."
        ),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default", "id": "id_ingress_namespace"},
            help_text="Namespace for the Ingress. Defaults to 'default'."
        ),
    )

    host = forms.CharField(
        label="Host",
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={
                "required": True,
                "placeholder": "example.com",
                "pattern": r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$",
                "title": "Must be a valid domain, e.g., example.com",
                "id": "id_ingress_host",
            },
            help_text="Fully qualified domain name for routing. Example: app.example.com"
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class IngressPathForm(forms.Form):
    path = forms.CharField(
        label="Path",
        max_length=200,
        widget=HelpButtonTextInput(
            attrs={"required": True, "placeholder": "/", "id": "id_path"},
            help_text="URL path to route traffic to the service. Example: / or /api"
        ),
    )

    service_name = forms.CharField(
        label="Service Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True, "id": "id_service_name"},
            help_text="The name of the Kubernetes Service to forward traffic to."
        ),
    )

    service_port = forms.IntegerField(
        label="Service Port",
        min_value=1,
        max_value=65535,
        widget=forms.NumberInput(attrs={"required": True, "id": "id_service_port"}),
        help_text="Port number on which the target Service is listening."
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class ServiceAccountForm(forms.Form):
    service_account_name = forms.CharField(
        label="ServiceAccount Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text="The name of the ServiceAccount resource to be created or referenced."
        ),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "default"},
            help_text="The namespace where the ServiceAccount resides. If omitted, 'default' will be used."
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class ImagePullSecretForm(forms.Form):
    secret_name = forms.CharField(
        label="Image Pull Secret Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text="The name of the Kubernetes secret used to authenticate when pulling images from a private registry."
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class RoleForm(forms.Form):
    role_type = forms.ChoiceField(
        label="Role Type",
        choices=[
            ("Role", "Role (namespaced)"),
            ("ClusterRole", "ClusterRole (cluster-wide)"),
        ],
        widget=forms.Select(attrs={"id": "id_role_type"}),
        help_text="Select 'Role' to apply permissions within a namespace or 'ClusterRole' for cluster-wide access."
    )

    role_name = forms.CharField(
        label="Role/ClusterRole Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text="The name of the Role or ClusterRole to create or bind to."
        ),
    )

    namespace = forms.CharField(
        label="Namespace (only for Role)",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_namespace_name", "placeholder": "Leave empty for ClusterRole,"},
            help_text="Required only when creating a Role. Leave empty for ClusterRoles."
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class RuleForm(forms.Form):
    api_groups = forms.CharField(
        label="API Groups (comma-separated, empty for core)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": ""},
            help_text="Comma-separated list of API groups this rule applies to. Leave empty for the core API group."
        ),
    )

    resources = forms.CharField(
        label="Resources (comma-separated)",
        required=True,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text="List of resource types (e.g., pods, services) this rule applies to."
        ),
    )

    verbs = forms.CharField(
        label="Verbs (comma-separated)",
        required=True,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text="Actions allowed: e.g., get, list, watch, create, delete, update."
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class RoleBindingForm(forms.Form):
    binding_name = forms.CharField(
        label="Binding Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text="The name of the RoleBinding or ClusterRoleBinding."
        ),
    )

    namespace_binding = forms.CharField(
        label="Namespace (only for RoleBinding)",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"id": "id_binding_namespace", "placeholder": "Leave empty for ClusterRoleBinding"},
            help_text="Specify the namespace only if creating a RoleBinding."
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class SubjectForm(forms.Form):
    kind = forms.ChoiceField(
        label="Subject Kind",
        choices=[
            ("User", "User"),
            ("Group", "Group"),
            ("ServiceAccount", "ServiceAccount"),
        ],
        help_text="Select the type of subject to bind: a User, a Group, or a ServiceAccount."
    )

    name = forms.CharField(
        label="Subject Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text="The name of the user, group, or service account to grant access to."
        ),
    )

    namespace = forms.CharField(
        label="Subject Namespace (only for ServiceAccount)",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "Only required for ServiceAccount"},
            help_text="Required only if the subject is a ServiceAccount. Leave empty otherwise."
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class NetworkPolicyForm(forms.Form):
    name = forms.CharField(
        label="NetworkPolicy Name",
        max_length=100,
        widget=HelpButtonTextInput(
            attrs={"required": True},
            help_text="The name of the NetworkPolicy resource. It must be unique within the namespace."
        ),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=HelpButtonTextInput(
            attrs={"required": False},
            help_text="The namespace to which this NetworkPolicy will apply. Defaults to 'default' if left blank."
        ),
    )

    pod_selector = forms.CharField(
        label="Pod Selector (key=value, comma-separated)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={
                "placeholder": "app=frontend,role=api",
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": "Format: key=value, separated by commas",
            },
            help_text="Selects the pods to which this policy applies. Format: key=value pairs separated by commas."
        ),
    )

    policy_types = forms.MultipleChoiceField(
        label="Policy Types",
        choices=[("Ingress", "Ingress"), ("Egress", "Egress")],
        widget=forms.CheckboxSelectMultiple,
        required=True,
        help_text="Choose one or both to specify the traffic direction: 'Ingress' for incoming or 'Egress' for outgoing."
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

class NetworkRuleForm(forms.Form):
    direction = forms.ChoiceField(
        label="Direction",
        choices=[("Ingress", "Ingress"), ("Egress", "Egress")],
        widget=forms.Select(attrs={"class": "direction-select"}),
        help_text="Defines the direction of traffic this rule applies to: Ingress (incoming) or Egress (outgoing)."
    )

    ports = forms.CharField(
        label="Ports (comma-separated)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={"pattern": r"^(\d{1,5})(,\d{1,5})*$"},
            help_text="List of ports to allow or restrict, separated by commas. Example: 80,443,8080"
        ),
    )

    pod_selector = forms.CharField(
        label="Pod Selector (key=value, comma-separated)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "role=db"},
            help_text="Applies the rule to traffic from/to pods matching these labels. Format: key=value"
        ),
    )

    namespace_selector = forms.CharField(
        label="Namespace Selector (key=value, comma-separated)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "env=prod"},
            help_text="Restrict the rule to namespaces matching these labels. Format: key=value"
        ),
    )

    ip_block = forms.CharField(
        label="IP Block (CIDR)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "192.168.1.0/24"},
            help_text="Specify a CIDR range to apply the rule to a set of IPs."
        ),
    )

    except_ips = forms.CharField(
        label="IP Exceptions (comma-separated CIDRs)",
        required=False,
        widget=HelpButtonTextInput(
            attrs={"placeholder": "192.168.1.5/32,192.168.1.6/32"},
            help_text="List of CIDR IPs to exclude from the IP block. Separate multiple entries with commas."
        ),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span style='color: black;'>* </span>")

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
            raise ValidationError("You must add at least one container.")
