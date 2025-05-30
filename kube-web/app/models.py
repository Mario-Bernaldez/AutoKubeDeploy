from django.db import models
from django.contrib.auth.models import User


class DeploymentHistory(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    resource_type = models.CharField(max_length=50)
    resource_name = models.CharField(max_length=100)
    yaml_content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.resource_type} - {self.resource_name} ({self.created_at})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    default_model = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"