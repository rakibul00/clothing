from django.db import models

class Branch(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name