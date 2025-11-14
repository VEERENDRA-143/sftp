from django.db import models

class FileMetadata(models.Model):
    filename = models.CharField(max_length=255)
    filepath = models.CharField(max_length=512)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
