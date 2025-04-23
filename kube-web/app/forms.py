# pylint=disable
# flake8: noqa

from app import utils
from django import forms
from django.forms import BaseFormSet, ValidationError, formset_factory

# --- Formularios auxiliares para puertos de servicios ---


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
        label="Node Port (solo para NodePort)",
        min_value=30000,
        max_value=32767,
        required=False,
        widget=forms.NumberInput(attrs={"class": "node-port-field"}),
    )


ServicePortFormSet = formset_factory(ServicePortForm, extra=1)

# --- Formularios principales ---


class ObjectTypeForm(forms.Form):
    object_type = forms.ChoiceField(
        label="Select Object Type",
        choices=[
            ("deployment", "Deployment"),
            ("namespace", "Namespace"),
            ("service", "Service"),
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
                "title": "Debe ser un número entero o un porcentaje (por ejemplo, 1 o 25%)",
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
                "title": "Debe ser un número entero o un porcentaje (por ejemplo, 1 o 25%)",
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
                "title": "Debe seguir el formato key=value, separados por comas.",
            }
        ),
    )


class ContainerForm(forms.Form):
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
                "title": "Debe seguir el formato key=value, separados por comas.",
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

    # Campos adicionales
    # EmptyDir
    medium = forms.CharField(
        label="Medium (for emptyDir)",
        required=False,
        validators=[utils.validate_medium],
        help_text="Deja vacío o escribe 'Memory' para usar memoria.",
        widget=forms.TextInput(
            attrs={
                "id": "id_medium",
                "pattern": r"^$|^Memory$",
                "title": "Deja vacío o escribe 'Memory' (respetando mayúsculas).",
            }
        ),
    )
    size_limit = forms.CharField(
        label="Size Limit (for emptyDir)",
        required=False,
        validators=[utils.validate_size_limit],
        help_text="Por ejemplo: 1Gi, 500Mi",
        widget=forms.TextInput(
            attrs={
                "id": "id_size_limit",
                "pattern": r"^\d+(Ki|Mi|Gi|Ti|Pi|Ei)$",
                "title": "Ingrese un tamaño válido como 1Gi, 500Mi, 100Ki, etc.",
            }
        ),
    )

    # HostPath
    path = forms.CharField(
        label="Path (for hostPath)",
        required=False,
        validators=[utils.validate_absolute_path],
        widget=forms.TextInput(
            attrs={
                "id": "id_path",
                "pattern": r"^/.*",
                "title": "Debe ser una ruta absoluta, por ejemplo: /data/volumen",
            }
        ),
    )
    HOSTPATH_TYPE_CHOICES = [
        ("", "— (vacío) —"),
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

    # PersistentVolumeClaim
    pvc_claim_name = forms.CharField(
        label="PVC Claim Name (for PersistentVolumeClaim)",
        required=False,
        widget=forms.TextInput(attrs={"id": "id_pvc_claim_name"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        vtype = cleaned_data.get("volume_type")

        if vtype == "hostPath" and not cleaned_data.get("path"):
            self.add_error("path", "Este campo es obligatorio para hostPath.")

        if vtype == "configMap" and not cleaned_data.get("config_map_name"):
            self.add_error(
                "config_map_name", "Este campo es obligatorio para configMap."
            )

        if vtype == "secret" and not cleaned_data.get("secret_name"):
            self.add_error("secret_name", "Este campo es obligatorio para Secret.")

        if vtype == "persistentVolumeClaim" and not cleaned_data.get("pvc_claim_name"):
            self.add_error(
                "pvc_claim_name",
                "Este campo es obligatorio para PersistentVolumeClaim.",
            )


class NamespaceForm(forms.Form):
    namespace_name = forms.CharField(label="Namespace Name", max_length=100)
    labels = forms.CharField(
        label="Namespace Labels (key=value, comma-separated)",
        required=False,
        widget=forms.TextInput(
            attrs={
                "pattern": r"^([^=\,]+=[^=\,]+)(,\s*[^=\,]+=[^=\,]+)*$",
                "title": "Debe seguir el formato key=value, separados por comas.",
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
                "title": "Debe seguir el formato key=value, separados por comas.",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        service_type = cleaned_data.get("service_type")
        return cleaned_data


class RequiredContainerFormSet(BaseFormSet):
    def clean(self):
        """
        Asegura que al menos un formulario de container esté rellenado y válido.
        """
        super().clean()

        if any(self.errors):
            # Si ya hay errores en los forms individuales, no hacemos más validaciones aquí
            return

        has_data = False
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                has_data = True
                break

        if not has_data:
            raise ValidationError("Debe agregar al menos un contenedor.")
