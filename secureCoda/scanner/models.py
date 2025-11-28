from django.db import models


class Document(models.Model):
    doc_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    last_scanned_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Table(models.Model):
    table_id = models.CharField(max_length=200)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.document.name} - {self.name}"


class Alert(models.Model):
    SEVERITY = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )
    document = models.OneToOneField(Document, on_delete=models.CASCADE)
    rule = models.CharField(max_length=255)
    severity = models.CharField(max_length=20, choices=SEVERITY)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.rule} ({self.severity})"
