from django.db import models


class DeploymentHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    resource_type = models.CharField(max_length=50)
    resource_name = models.CharField(max_length=100)
    yaml_content = models.TextField()

    def __str__(self):
        return f"{self.resource_type} - {self.resource_name} ({self.created_at})"
