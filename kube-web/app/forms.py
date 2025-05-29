# pylint: disable
# flake8: noqa

from app import utils
from django import forms
from django.forms import BaseFormSet, ValidationError, formset_factory

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
        widget=forms.NumberInput(attrs={"required": "required"}),
    )
    target_port = forms.IntegerField(
        label="Target Port",
        min_value=1,
        max_value=65535,
        widget=forms.NumberInput(attrs={"required": "required"}),
    )
    protocol = forms.ChoiceField(label="Protocol", choices=PROTOCOL_CHOICES)
    node_port = forms.IntegerField(
        label="Node Port (only for NodePort)",
        min_value=30000,
        max_value=32767,
        required=False,
        widget=forms.NumberInput(attrs={"class": "node-port-field"}),
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
    name = forms.CharField(label="Deployment Name", max_length=100)
    namespace = forms.CharField(label="Namespace", max_length=100, required=False)
    replicas = forms.IntegerField(label="Replicas", min_value=1, initial=1)

    STRATEGY_CHOICES = [("RollingUpdate", "Rolling Update"), ("Recreate", "Recreate")]
    strategy = forms.ChoiceField(label="Deployment Strategy", choices=STRATEGY_CHOICES)

    max_unavailable = forms.CharField(
        label="Max Unavailable (RollingUpdate)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "id_max_unavailable",
                "pattern": r"^\d+%?$",
                "title": "Must be an integer or percentage (e.g. 1 or 25%)",
            }
        ),
        validators=[utils.validate_int_or_percent],
        initial="1",
    )

    max_surge = forms.CharField(
        label="Max Surge (RollingUpdate)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "id_max_surge",
                "pattern": r"^\d+%?$",
                "title": "Must be an integer or percentage (e.g. 1 or 25%)",
            }
        ),
        validators=[utils.validate_int_or_percent],
        initial="1",
    )


class PodTemplateForm(forms.Form):
    pod_name = forms.CharField(label="Pod Name", max_length=100, required=False)
    labels = forms.CharField(
        label="Pod Labels (key=value, comma-separated)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": "Must follow the format key=value, comma-separated.",
            }
        ),
    )


class ContainerForm(forms.Form):
    init_container = forms.BooleanField(
        label="Is Init Container?",
        required=False,
    )
    container_name = forms.CharField(
        label="Container Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )

    image = forms.CharField(
        label="Container Image",
        max_length=200,
        widget=forms.TextInput(attrs={"required": True}),
    )

    IMAGE_PULL_POLICY_CHOICES = [
        ("Always", "Always"),
        ("IfNotPresent", "If Not Present"),
        ("Never", "Never"),
    ]
    image_pull_policy = forms.ChoiceField(
        label="Image Pull Policy", choices=IMAGE_PULL_POLICY_CHOICES
    )

    ports = forms.CharField(
        label="Ports (comma-separated numbers)",
        required=False,
        validators=[utils.validate_ports],
        widget=forms.TextInput(
            attrs={
                "pattern": r"^(\d{1,5})(,\d{1,5})*$",
            }
        ),
    )

    env_vars = forms.CharField(
        label="Environment Variables (key=value, comma-separated)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": "Must follow the format key=value, comma-separated.",
            }
        ),
    )


class VolumeMountForm(forms.Form):
    volume_name = forms.CharField(label="Volume Name", max_length=100)
    mount_path = forms.CharField(label="Mount Path", max_length=200)


class VolumeForm(forms.Form):
    volume_name = forms.CharField(label="Volume Name", max_length=100)
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
    )

    # EmptyDir fields
    medium = forms.CharField(
        label="Medium (for emptyDir)",
        required=False,
        validators=[utils.validate_medium],
        help_text="Leave empty or enter 'Memory' to use memory.",
        widget=forms.TextInput(
            attrs={
                "id": "id_medium",
                "pattern": r"^$|^Memory$",
                "title": "Leave empty or enter 'Memory' (case-sensitive).",
            }
        ),
    )
    size_limit = forms.CharField(
        label="Size Limit (for emptyDir)",
        required=False,
        validators=[utils.validate_size_limit],
        help_text="Example: 1Gi, 500Mi",
        widget=forms.TextInput(
            attrs={
                "id": "id_size_limit",
                "pattern": r"^\d+(Ki|Mi|Gi|Ti|Pi|Ei)$",
                "title": "Enter a valid size such as 1Gi, 500Mi, 100Ki, etc.",
            }
        ),
    )

    # HostPath fields
    path = forms.CharField(
        label="Path (for hostPath)",
        required=False,
        validators=[utils.validate_absolute_path],
        widget=forms.TextInput(
            attrs={
                "id": "id_path",
                "pattern": r"^/.*",
                "title": "Must be an absolute path, e.g. /data/volume",
            }
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
    )

    # ConfigMap
    config_map_name = forms.CharField(
        label="ConfigMap Name (for configMap)",
        required=False,
        widget=forms.TextInput(attrs={"id": "id_config_map_name"}),
    )

    # Secret
    secret_name = forms.CharField(
        label="Secret Name (for Secret)",
        required=False,
        widget=forms.TextInput(attrs={"id": "id_secret_name"}),
    )

    # PVC
    pvc_claim_name = forms.CharField(
        label="PVC Claim Name (for PersistentVolumeClaim)",
        required=False,
        widget=forms.TextInput(attrs={"id": "id_pvc_claim_name"}),
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
            self.add_error(
                "pvc_claim_name", "This field is required for PersistentVolumeClaim."
            )


class NamespaceForm(forms.Form):
    namespace_name = forms.CharField(label="Namespace Name", max_length=100)
    labels = forms.CharField(
        label="Namespace Labels (key=value, comma-separated)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": "Must follow the format key=value, comma-separated.",
            }
        ),
    )


class ServiceForm(forms.Form):
    service_name = forms.CharField(label="Service Name", max_length=100)
    service_type = forms.ChoiceField(
        label="Service Type",
        choices=[
            ("ClusterIP", "ClusterIP"),
            ("NodePort", "NodePort"),
            ("LoadBalancer", "LoadBalancer"),
        ],
    )
    selector = forms.CharField(
        label="Service Selector (key=value, comma-separated)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": "Must follow the format key=value, comma-separated.",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        service_type = cleaned_data.get("service_type")
        return cleaned_data


class HPAForm(forms.Form):
    hpa_name = forms.CharField(
        label="HPA Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "default"}),
    )

    target_deployment = forms.CharField(
        label="Target Deployment Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )

    min_replicas = forms.IntegerField(
        label="Minimum Replicas",
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={"required": True}),
    )

    max_replicas = forms.IntegerField(
        label="Maximum Replicas",
        min_value=1,
        widget=forms.NumberInput(attrs={"required": True}),
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


class HPAMetricForm(forms.Form):
    resource_name = forms.ChoiceField(
        label="Resource Name",
        choices=[("cpu", "CPU"), ("memory", "Memory")],
    )

    target_type = forms.ChoiceField(
        label="Target Type",
        choices=[("Utilization", "Utilization (%)"), ("Value", "Value (absolute)")],
    )

    target_value = forms.IntegerField(
        label="Target Value",
        min_value=1,
        widget=forms.NumberInput(attrs={"required": True}),
        help_text="Use a percentage for Utilization or an absolute number for Value.",
    )


class ConfigMapForm(forms.Form):
    configmap_name = forms.CharField(
        label="ConfigMap Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )
    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "default"}),
    )


class ConfigMapKeyForm(forms.Form):
    key_name = forms.CharField(
        label="Key",
        max_length=200,
        widget=forms.TextInput(attrs={"required": True}),
    )
    is_multiline = forms.BooleanField(
        label="Multiline content (like file data)?",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(),
    )
    value = forms.CharField(
        label="Value",
        widget=forms.Textarea(attrs={"rows": 3, "required": True}),
    )


class SecretForm(forms.Form):
    secret_name = forms.CharField(
        label="Secret Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )
    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "default"}),
    )
    secret_type = forms.ChoiceField(
        label="Secret Type",
        choices=[
            ("Opaque", "Opaque (key-value)"),
            ("kubernetes.io/tls", "TLS (Certificate and Private Key)"),
            (
                "kubernetes.io/dockerconfigjson",
                "Docker Config JSON (.dockerconfigjson)",
            ),
        ],
        widget=forms.Select(attrs={"id": "id_secret_type"}),
    )


class OpaqueKeyForm(forms.Form):
    key_name = forms.CharField(
        label="Key",
        max_length=200,
        widget=forms.TextInput(attrs={"required": True}),
    )
    value = forms.CharField(
        label="Value",
        widget=forms.TextInput(attrs={"required": True}),
    )


class TLSSecretForm(forms.Form):
    tls_crt = forms.CharField(
        label="TLS Certificate (tls.crt)",
        widget=forms.Textarea(attrs={"rows": 4, "required": True}),
    )
    tls_key = forms.CharField(
        label="TLS Private Key (tls.key)",
        widget=forms.Textarea(attrs={"rows": 4, "required": True}),
    )


class DockerConfigJSONForm(forms.Form):
    dockerconfigjson = forms.CharField(
        label="Docker Config JSON (.dockerconfigjson)",
        widget=forms.Textarea(attrs={"rows": 8, "required": True}),
        help_text="Paste the complete Docker config JSON content here.",
    )


class PersistentVolumeClaimForm(forms.Form):
    pvc_name = forms.CharField(
        label="PVC Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "default"}),
    )

    storage_request = forms.CharField(
        label="Requested Storage (e.g., 1Gi, 500Mi)",
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "required": True,
                "pattern": r"^\d+(Ki|Mi|Gi|Ti|Pi|Ei)$",
                "title": "Must be a valid size like 1Gi, 500Mi, 100Ki, etc.",
            }
        ),
        help_text="Use units like Mi, Gi, Ti, etc.",
    )

    access_modes = forms.MultipleChoiceField(
        label="Access Modes",
        choices=[
            ("ReadWriteOnce", "ReadWriteOnce"),
            ("ReadOnlyMany", "ReadOnlyMany"),
            ("ReadWriteMany", "ReadWriteMany"),
        ],
        widget=forms.CheckboxSelectMultiple,
        help_text="You can select one or more access modes.",
    )

    storage_class_name = forms.CharField(
        label="Storage Class Name (Optional)",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Leave empty for default"}),
    )


class IngressForm(forms.Form):
    ingress_name = forms.CharField(
        label="Ingress Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "default"}),
    )

    host = forms.CharField(
        label="Host",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "required": True,
                "placeholder": "example.com",
                "pattern": r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$",
                "title": "Must be a valid domain, e.g., example.com",
            }
        ),
    )


class IngressPathForm(forms.Form):
    path = forms.CharField(
        label="Path",
        max_length=200,
        widget=forms.TextInput(attrs={"required": True, "placeholder": "/"}),
    )

    service_name = forms.CharField(
        label="Service Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )

    service_port = forms.IntegerField(
        label="Service Port",
        min_value=1,
        max_value=65535,
        widget=forms.NumberInput(attrs={"required": True}),
    )


class ServiceAccountForm(forms.Form):
    service_account_name = forms.CharField(
        label="ServiceAccount Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "default"}),
    )


class ImagePullSecretForm(forms.Form):
    secret_name = forms.CharField(
        label="Image Pull Secret Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )


class RoleForm(forms.Form):
    role_type = forms.ChoiceField(
        label="Role Type",
        choices=[
            ("Role", "Role (namespaced)"),
            ("ClusterRole", "ClusterRole (cluster-wide)"),
        ],
        widget=forms.Select(attrs={"id": "id_role_type"}),
    )

    role_name = forms.CharField(
        label="Role/ClusterRole Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )

    namespace = forms.CharField(
        label="Namespace (only for Role)",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Leave empty for ClusterRole"}),
    )


class RuleForm(forms.Form):
    api_groups = forms.CharField(
        label="API Groups (comma-separated, empty for core)",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": ""}),
    )
    resources = forms.CharField(
        label="Resources (comma-separated)",
        required=True,
        widget=forms.TextInput(attrs={"required": True}),
    )
    verbs = forms.CharField(
        label="Verbs (comma-separated)",
        required=True,
        widget=forms.TextInput(attrs={"required": True}),
        help_text="Examples: get, list, watch, create, delete",
    )


class RoleBindingForm(forms.Form):
    binding_name = forms.CharField(
        label="Binding Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )

    namespace = forms.CharField(
        label="Namespace (only for RoleBinding)",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Leave empty for ClusterRoleBinding"}
        ),
    )


class SubjectForm(forms.Form):
    kind = forms.ChoiceField(
        label="Subject Kind",
        choices=[
            ("User", "User"),
            ("Group", "Group"),
            ("ServiceAccount", "ServiceAccount"),
        ],
    )
    name = forms.CharField(
        label="Subject Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )
    namespace = forms.CharField(
        label="Subject Namespace (only for ServiceAccount)",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "Only required for ServiceAccount"}
        ),
    )


class NetworkPolicyForm(forms.Form):
    name = forms.CharField(
        label="NetworkPolicy Name",
        max_length=100,
        widget=forms.TextInput(attrs={"required": True}),
    )

    namespace = forms.CharField(
        label="Namespace",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"required": False}),
    )

    pod_selector = forms.CharField(
        label="Pod Selector (key=value, comma-separated)",
        widget=forms.TextInput(
            attrs={
                "placeholder": "app=frontend,role=api",
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": "Format: key=value, separated by commas",
            }
        ),
        required=False,
    )

    policy_types = forms.MultipleChoiceField(
        label="Policy Types",
        choices=[("Ingress", "Ingress"), ("Egress", "Egress")],
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )


class NetworkRuleForm(forms.Form):
    direction = forms.ChoiceField(
        label="Direction",
        choices=[("Ingress", "Ingress"), ("Egress", "Egress")],
        widget=forms.Select(attrs={"class": "direction-select"}),
    )

    ports = forms.CharField(
        label="Ports (comma-separated)",
        required=False,
        help_text="e.g., 80,443,8080",
        widget=forms.TextInput(attrs={"pattern": r"^(\d{1,5})(,\d{1,5})*$"}),
    )

    pod_selector = forms.CharField(
        label="Pod Selector (key=value, comma-separated)",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "role=db"}),
    )

    namespace_selector = forms.CharField(
        label="Namespace Selector (key=value, comma-separated)",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "env=prod"}),
    )

    ip_block = forms.CharField(
        label="IP Block (CIDR)",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "192.168.1.0/24"}),
    )

    except_ips = forms.CharField(
        label="IP Exceptions (comma-separated CIDRs)",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "192.168.1.5/32,192.168.1.6/32"}),
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
            raise ValidationError("You must add at least one container.")
