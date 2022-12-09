from django.db import models
from django.utils import timezone


class Audio(models.Model):
    audio = models.FileField(upload_to='audios/')
    created_on = models.DateTimeField(default=timezone.now)
    num_speakers = models.IntegerField()
    transcript = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Audio: {self.audio}"

class Speaker(models.Model):
    name = models.CharField(max_length=128)
    model = models.FileField(upload_to='models/')
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Speaker: {self.name}"
