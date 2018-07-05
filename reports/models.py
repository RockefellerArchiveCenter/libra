from datetime import datetime
from urllib.parse import urljoin

from django.db import models

from reports.clients import FedoraClient


class Report(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    PROCESS_STATUS_CHOICES = (
        ("queued", "Report queued"),
        ("started", "Report started"),
        ("completed", "Report completed"),
    )
    process_status = models.CharField(choices=PROCESS_STATUS_CHOICES, max_length=100)
    items_checked = models.PositiveIntegerField(default=0)


class ReportItem(models.Model):
    file = models.CharField(max_length=512)
    uri = models.CharField(max_length=512)
    created = models.DateTimeField(auto_now_add=True)


class FixityReport(Report):

    def __init__(self):
        report = FixityReport.objects.create(
            process_status='started'
        )
        client = FedoraClient()

    def run(self):
        print("Running {}".format(self))
        for path in file_paths:  # not sure how we get file paths yet
            fixity = client.check_fixity(path)
            if not fixity.verdict:
                FixityReportItem.objects.create(
                    report=report,
                    file=resp['file'],
                    uri=path,
                    stored_checksum=resp['stored_checksum'],
                    calculated_checksum=resp['calculated_checksum'],
                )
            report.items_checked += 1
        report.process_status = 'completed'
        report.end_time = datetime.now()
        report.save()


class FixityReportItem(models.Model):
    report = models.ForeignKey(FixityReport, on_delete=models.CASCADE, related_name="report")
    stored_checksum = models.CharField(max_length=512)
    calculated_checksum = models.CharField(max_length=512)


class FormatReport(Report):

    def __init__(self):
        report = FormatReport.objects.create(
            process_status='started'
        )
        client = FedoraClient()

    def run(self):
        print("Running {}".format(self))
        for path in file_paths:  # not sure how we get file paths yet
            resp = client.get(path)
            FormatReportItem.objects.create(
                report=report,
                file=resp['file'],
                uri=path,
                file_format=resp['format'],
            )
            report.items_checked += 1
        report.process_status = 'completed'
        report.end_time = datetime.now()
        report.save()


class FormatReportItem(models.Model):
    report = models.ForeignKey(FormatReport, on_delete=models.CASCADE, related_name="report")
    file_format = models.CharField(max_length=256)
