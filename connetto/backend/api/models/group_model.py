import uuid
from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    identifier = models.CharField(
        max_length=36,
        unique=True,
        default=uuid.uuid4,  # ユニークなデフォルト値を設定
        editable=False
    )
    meeting_date = models.DateTimeField() 
    meeting_location = models.CharField(max_length=100) 
    leader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="leader_of_groups"
    )
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Group {self.identifier} ({self.meeting_date} @ {self.meeting_location})"