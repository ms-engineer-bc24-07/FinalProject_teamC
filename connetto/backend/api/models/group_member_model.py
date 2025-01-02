from django.db import models
from django.contrib.auth.models import User

class GroupMember(models.Model):
    group = models.ForeignKey(
        'Group', 
        on_delete=models.CASCADE,
        related_name="members"
    )  
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="group_memberships"
    ) 
    is_leader = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} in Group {self.group.identifier}"
