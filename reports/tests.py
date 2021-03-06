import json
import random
import string
import vcr

from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APIRequestFactory

from libra import settings
from reports.cron import RunReports
from reports.models import Report, FixityReportItem, FormatReportItem
from reports.views import FixityReportViewSet, FormatReportViewSet, ReportRunView

reports_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='fixtures/cassettes',
    record_mode='once',
    match_on=['path', 'method'],
    filter_query_parameters=['username', 'password'],
    filter_headers=['Authorization'],
)


class ReportTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = Client()
        self.format_report_count = 4
        self.format_report_items_count = 25
        self.fixity_report_count = 2
        self.fixity_report_items_count = 10

    def create_reports(self):
        print('*** Creating Reports ***')
        for i in range(self.format_report_count):
            request = self.factory.post(reverse('formatreport-list'), format='json')
            response = FormatReportViewSet.as_view(actions={"post": "create"})(request)
            print('Created format report {url}'.format(url=response.data['url']))
            self.assertEqual(response.status_code, 200, "Wrong HTTP code")
        for i in range(self.fixity_report_count):
            request = self.factory.post(reverse('fixityreport-list'), format='json')
            response = FixityReportViewSet.as_view(actions={"post": "create"})(request)
            print('Created fixity report {url}'.format(url=response.data['url']))
            self.assertEqual(response.status_code, 200, "Wrong HTTP code")
        self.assertEqual(len(Report.objects.filter(report_type='fixity')), self.fixity_report_count, "Wrong number of fixity reports created")
        self.assertEqual(len(Report.objects.filter(report_type='format')), self.format_report_count, "Wrong number of format reports created")
        for report in Report.objects.all():
            self.assertEqual(report.process_status, 'queued', "Report process status not correctly set")
            self.assertIsNot(report.start_time, False, "Report start time not added")

    def create_report_items(self):
        print('*** Creating Report Items ***')
        format_report = random.choice(Report.objects.filter(report_type='format'))
        fixity_report = random.choice(Report.objects.filter(report_type='fixity'))
        for i in range(self.format_report_items_count):
            FormatReportItem.objects.create(
                report=format_report,
                file=''.join(random.choices(string.ascii_letters + string.digits, k=25)),
                uri=''.join(random.choices(string.ascii_letters + string.digits, k=20)),
                file_format=''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            )
        for i in range(self.fixity_report_items_count):
            FixityReportItem.objects.create(
                report=fixity_report,
                file=''.join(random.choices(string.ascii_letters + string.digits, k=25)),
                uri=''.join(random.choices(string.ascii_letters + string.digits, k=20)),
                verdict=random.choice([True, False]),
            )
        self.assertEqual(len(Report.objects.filter(report_type='fixity')), self.fixity_report_count, "Wrong number of fixity reports created")
        self.assertEqual(len(Report.objects.filter(report_type='format')), self.format_report_count, "Wrong number of format reports created")

    def run_reports(self):
        print('*** Running Reports ***')
        with reports_vcr.use_cassette('run_reports.yml'):
            RunReports().do()
        for report in Report.objects.all():
            self.assertEqual(report.process_status, 'completed', 'Report was not completed')
            self.assertNotEqual(report.start_time, None, 'Start time not added')
            self.assertNotEqual(report.end_time, None, 'End time not added')

    def delete_reports(self):
        print('*** Deleting Reports ***')
        format_report = random.choice(Report.objects.filter(report_type='format'))
        fixity_report = random.choice(Report.objects.filter(report_type='fixity'))
        request = self.factory.delete(reverse('fixityreport-detail', kwargs={'pk': fixity_report.pk}), format='json')
        response = FixityReportViewSet.as_view(actions={"delete": "destroy"})(request, pk=fixity_report.pk)
        print('Deleted fixity report')
        self.assertEqual(response.status_code, 204, "Wrong HTTP code")
        request = self.factory.delete(reverse('formatreport-detail', kwargs={'pk': format_report.pk}), format='json')
        response = FormatReportViewSet.as_view(actions={"delete": "destroy"})(request, pk=format_report.pk)
        print('Deleted format report')
        self.assertEqual(response.status_code, 204, "Wrong HTTP code")
        self.assertEqual(len(Report.objects.filter(report_type='fixity')), self.fixity_report_count-1, "Wrong number of fixity reports created")
        self.assertEqual(len(Report.objects.filter(report_type='format')), self.format_report_count-1, "Wrong number of format reports created")

    def run_endpoints(self):
        print('*** Testing run endpoints ***')
        with reports_vcr.use_cassette('run_reports.yml'):
            for report_type in ['fixity', 'format']:
                request = self.factory.post(reverse('run-reports', kwargs={"report": report_type}))
                response = ReportRunView.as_view()(request, report=report_type)
                self.assertEqual(response.status_code, 200, "Wrong HTTP code")

    def schema(self):
        print('*** Getting schema view ***')
        schema = self.client.get(reverse('schema-json', kwargs={"format": ".json"}))
        self.assertEqual(schema.status_code, 200, "Wrong HTTP code")

    def health_check(self):
        print('*** Getting status view ***')
        status = self.client.get(reverse('api_health_ping'))
        self.assertEqual(status.status_code, 200, "Wrong HTTP code")

    def test_reports(self):
        self.create_reports()
        self.create_report_items()
        self.run_reports()
        self.delete_reports()
        self.run_endpoints()
        self.schema()
        self.health_check()
