from urllib.parse import urljoin

from django.db import models
from django.utils import timezone

from libra import config as CF

from reports.clients import FedoraClient


class Report(models.Model):
    created_time = models.DateTimeField(auto_now_add=True) # Datetime the report was created
    queued_time = models.DateTimeField(null=True, blank=True) # Datetime the report should be started
    start_time = models.DateTimeField(null=True, blank=True) # Datetime the report was started
    end_time = models.DateTimeField(null=True, blank=True) # Datetime the report finished
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

    def get_type(self): return 'fixity'

    def process_children(self, resources):
        for r in resources:
            if r.__class__.__name__ == 'NonRDFSource':
                print("Creating report item for {}".format(r.uri))
                fixity = self.client.check_fixity(r.uri)
                FixityReportItem.objects.create(
                    report=self,
                    verdict=fixity['verdict'],
                    uri=r.uri,
                )
                self.items_checked += 1
            if len(r.children()) > 0:
                self.process_children(r.children(as_resources=True))

    def run(self):
        self.client = FedoraClient()
        print("Running {}".format(self))
        self.process_status = 'started'
        self.start_time = timezone.now()
        self.save()
        base_resource = self.client.get_resource(CF.FEDORA['baseurl'])
        children = base_resource.children(as_resources=True)
        self.process_children(children)
        self.process_status = 'completed'
        self.end_time = timezone.now()
        self.save()


class FixityReportItem(ReportItem):
    report = models.ForeignKey(FixityReport, on_delete=models.CASCADE, related_name="report")
    verdict = models.CharField(max_length=10)


class FormatReport(Report):

    def get_type(self): return 'format'

    def process_children(self, resources):
        for r in resources:
            if r.__class__.__name__ == 'NonRDFSource':
                print("Creating report item for {}".format(r.uri))
                FormatReportItem.objects.create(
                    report=self,
                    uri=r.uri,
                    file_format=r.binary.mimetype,
                )
                self.items_checked += 1
        if len(r.children()) > 0:
            self.process_children(r.children(as_resources=True))

    def run(self):
        self.client = FedoraClient()
        print("Running {}".format(self))
        self.process_status = 'started'
        self.start_time = timezone.now()
        self.save()
        base_resource = self.client.get_resource(CF.FEDORA['baseurl'])
        children = base_resource.children(as_resources=True)
        self.process_children(children)
        self.process_status = 'completed'
        self.end_time = timezone.now()
        self.save()


class FormatReportItem(ReportItem):
    report = models.ForeignKey(FormatReport, on_delete=models.CASCADE, related_name="report")
    file_format = models.CharField(max_length=256)
