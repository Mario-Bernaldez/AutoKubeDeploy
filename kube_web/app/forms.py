from django import forms

class ObjectTypeForm(forms.Form):
    object_type = forms.ChoiceField(
        label="Select Object Type",
        choices=[
            ('deployment', 'Deployment'),
            ('namespace', 'Namespace'),
            ('service', 'Service')
        ],
        widget=forms.RadioSelect
    )

class DeploymentForm(forms.Form):
    name = forms.CharField(label="Deployment Name", max_length=100)
    namespace = forms.CharField(label="Namespace", max_length=100, required=False)
    replicas = forms.IntegerField(label="Replicas", min_value=1, initial=1)

    STRATEGY_CHOICES = [
        ('RollingUpdate', 'Rolling Update'),
        ('Recreate', 'Recreate')
    ]
    strategy = forms.ChoiceField(label="Deployment Strategy", choices=STRATEGY_CHOICES)

    max_unavailable = forms.IntegerField(label="Max Unavailable (RollingUpdate)", required=False)
    max_surge = forms.IntegerField(label="Max Surge (RollingUpdate)", required=False)

class PodTemplateForm(forms.Form):
    pod_name = forms.CharField(label="Pod Name", max_length=100, required=False)
    labels = forms.CharField(label="Pod Labels (key=value, comma-separated)", required=False)

class ContainerForm(forms.Form):
    container_name = forms.CharField(label="Container Name", max_length=100)
    image = forms.CharField(label="Container Image", max_length=200)
    
    IMAGE_PULL_POLICY_CHOICES = [
        ('Always', 'Always'),
        ('IfNotPresent', 'If Not Present'),
        ('Never', 'Never')
    ]
    image_pull_policy = forms.ChoiceField(label="Image Pull Policy", choices=IMAGE_PULL_POLICY_CHOICES)

    ports = forms.CharField(label="Ports (comma-separated numbers)", required=False)
    env_vars = forms.CharField(label="Environment Variables (key=value, comma-separated)", required=False)

class VolumeMountForm(forms.Form):
    volume_name = forms.CharField(label="Volume Name", max_length=100)
    mount_path = forms.CharField(label="Mount Path", max_length=200)

class VolumeForm(forms.Form):
    volume_name = forms.CharField(label="Volume Name", max_length=100)
    volume_type = forms.ChoiceField(label="Volume Type", choices=[
        ('emptyDir', 'emptyDir'),
        ('hostPath', 'hostPath'),
        ('configMap', 'configMap'),
        ('secret', 'Secret'),
        ('persistentVolumeClaim', 'PersistentVolumeClaim')
    ])

class NamespaceForm(forms.Form):
    namespace_name = forms.CharField(label="Namespace Name", max_length=100)
    labels = forms.CharField(label="Namespace Labels (key=value, comma-separated)", required=False)

class ServiceForm(forms.Form):
    service_name = forms.CharField(label="Service Name", max_length=100)
    service_type = forms.ChoiceField(label="Service Type", choices=[
        ('ClusterIP', 'ClusterIP'),
        ('NodePort', 'NodePort'),
        ('LoadBalancer', 'LoadBalancer')
    ])
    ports = forms.CharField(label="Service Ports (comma-separated)", required=False)
    selector = forms.CharField(label="Service Selector (key=value, comma-separated)", required=False)