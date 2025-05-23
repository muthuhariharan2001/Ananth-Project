from django.db import models

class ImageHashDBA(models.Model):
    hash = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.hash

class ImageHashDBB(models.Model):
    hash = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.hash

class HashPair(models.Model):
    dba_hash = models.ForeignKey(ImageHashDBA, on_delete=models.CASCADE)
    dbb_hash = models.ForeignKey(ImageHashDBB, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('dba_hash', 'dbb_hash') 

    def __str__(self):
        return f"{self.dba_hash.hash} ↔ {self.dbb_hash.hash}"
