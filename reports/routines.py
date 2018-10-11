from urllib.parse import urljoin
from django.utils import timezone

from libra import config as CF

from reports.clients import FedoraClient
from reports.models import Report, FixityReportItem, FormatReportItem

class ReportRunnerException: pass


class ReportRunner:
    def __init__(self):
        self.client = FedoraClient()
        self.base_resource = self.client.get_resource(CF.FEDORA['baseurl'])

    def run(self, report_type):
        try:
            current_time = timezone.now()
            reports = Report.objects.filter(report_type=report_type,
                                            process_status='queued',
                                            queued_time__lte=current_time)
            for report in reports:
                report.process_status = 'started'
                report.start_time = timezone.now()
                report.save()
                children = self.base_resource.children(as_resources=True)
                self.process_children(children, report)
                report.process_status = 'completed'
                report.end_time = timezone.now()
                report.save()
        except Exception as e:
            raise ReportRunnerException("Error running report: {}".format(e))

    def process_children(self, resources, report):
        for r in resources:
            if r.__class__.__name__ == 'NonRDFSource':
                if report.report_type == 'fixity':
                    fixity = r.fixity()
                    FixityReportItem.objects.create(
                        report=report,
                        verdict=fixity['verdict'],
                        uri=r.uri,
                    )
                elif report.report_type == 'format':
                    FormatReportItem.objects.create(
                        report=report,
                        uri=r.uri,
                        file_format=r.binary.mimetype,
                    )
                report.items_checked += 1
            if len(r.children()) > 0:
                self.process_children(r.children(as_resources=True), report)
