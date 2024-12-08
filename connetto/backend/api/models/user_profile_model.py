from django.db import models

GENDER_CHOICES = [
    ("male", "男性"),
    ("female", "女性"),
]
class UserProfile(models.Model):
    username = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    furigana = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    birth_year = models.IntegerField()
    join_year = models.IntegerField()
    department = models.CharField(max_length=50)
    station = models.CharField(max_length=50)

    def __str__(self):
        return self.username
