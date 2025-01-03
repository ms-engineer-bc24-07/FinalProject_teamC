from django.db import models
from .group_model import Group

class Restaurant(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="shop_options"
    )
    name = models.CharField(max_length=100)
    url = models.URLField()
    address = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    is_selected = models.BooleanField(default=False)
    opening_hours = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Group {self.group.identifier})"
