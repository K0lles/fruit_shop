from django.db import models


class Declaration(models.Model):
    document = models.FileField(upload_to='declarations/')
