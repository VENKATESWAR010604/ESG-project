from django.db import models


class IngestionBatch(models.Model):
    SOURCE_CHOICES = [
        ("SAP", "SAP"),
        ("UTILITY", "Utility"),
        ("TRAVEL", "Travel"),
    ]

    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    total_rows = models.IntegerField(default=0)
    failed_rows = models.IntegerField(default=0)
    suspicious_rows = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_type} - {self.created_at}"


class ActivityRow(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("FAILED", "Failed"),
        ("SUSPICIOUS", "Suspicious"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    ]

    SCOPE_CHOICES = [
        ("SCOPE_1", "Scope 1"),
        ("SCOPE_2", "Scope 2"),
        ("SCOPE_3", "Scope 3"),
    ]

    batch = models.ForeignKey(
        IngestionBatch,
        on_delete=models.CASCADE,
        related_name="rows"
    )

    source_type = models.CharField(max_length=20)

    raw_data = models.JSONField()
    normalized_data = models.JSONField(blank=True, null=True)

    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, blank=True, null=True)
    activity_type = models.CharField(max_length=100, blank=True, null=True)

    quantity = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    error_reason = models.TextField(blank=True, null=True)
    suspicious_reason = models.TextField(blank=True, null=True)

    is_locked = models.BooleanField(default=False)

    approved_at = models.DateTimeField(blank=True, null=True)
    rejected_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source_type} - {self.status}"


class AuditLog(models.Model):
    row = models.ForeignKey(
        ActivityRow,
        on_delete=models.CASCADE,
        related_name="audit_logs"
    )
    action = models.CharField(max_length=50)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - Row {self.row.id}"