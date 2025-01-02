from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

class NotificationType(models.TextChoices):
    REGISTER = "REGISTER", "登録完了"
    UPDATE = "UPDATE", "登録内容変更"
    DELETE = "DELETE", "登録内容削除"
    EVENT_DECISION = "EVENT_DECISION", "開催決定"
    MANAGER_DECISION = "MANAGER_DECISION", "幹事決定"
    EVENT_DETAIL = "EVENT_DETAIL", "詳細決定"
    REMINDER_MANAGER = "REMINDER_MANAGER", "予約期限間近のご案内"
    REMINDER_EVENT = "REMINDER_EVENT", "当日のご案内"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    title = models.CharField(max_length=255)  
    body = models.TextField() 
    data = models.JSONField(null=True, blank=True)
    is_read = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True) 

    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.REGISTER,
    )

    def __str__(self):
        return f"{self.title} - {self.user.username}" 

