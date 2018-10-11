import logging
from structlog import wrap_logger
from uuid import uuid4

from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView, TemplateView, View

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from reports.formatmixins import CSVResponseMixin
from reports.models import Report, FixityReportItem, FormatReportItem
from reports.routines import ReportRunner
from reports.serializers import FixityReportSerializer, FormatReportSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger = wrap_logger(logger)


class DashboardView(TemplateView):
    template_name = 'reports/main.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['fixity_reports'] = {}
        context['format_reports'] = {}
        context['fixity_reports']['objects'] = Report.objects.filter(report_type='fixity')
        context['fixity_reports']['running'] = Report.objects.filter(report_type='fixity', process_status='started').count()
        context['fixity_reports']['queued'] = Report.objects.filter(report_type='fixity', process_status='queued').count()
        context['fixity_reports']['completed'] = Report.objects.filter(report_type='fixity', process_status='completed').count()
        context['format_reports']['objects'] = Report.objects.filter(report_type='format')
        context['format_reports']['running'] = Report.objects.filter(report_type='format', process_status='started').count()
        context['format_reports']['queued'] = Report.objects.filter(report_type='format', process_status='queued').count()
        context['format_reports']['completed'] = Report.objects.filter(report_type='format', process_status='completed').count()
        return context


class FixityReportListView(ListView):
    queryset = Report.objects.filter(report_type='fixity')
    template_name = 'reports/list.html'

    def get_context_data(self, **kwargs):
        context = super(FixityReportListView, self).get_context_data(**kwargs)
        context['running'] = Report.objects.filter(report_type='fixity', process_status='started').order_by('-start_time')
        context['queued'] = Report.objects.filter(report_type='fixity', process_status='queued').order_by('-start_time')
        context['completed'] = Report.objects.filter(report_type='fixity', process_status='completed').order_by('-end_time')
        return context


class FixityReportDataView(CSVResponseMixin, View):
    model = Report

    def get(self, request, *args, **kwargs):
        data = [('File', 'URI', 'Fixity Verdict', 'Time Checked',)]
        items = FixityReportItem.objects.filter(report=kwargs['pk'])
        print(items)
        for item in items:
            data.append((
                item.file,
                item.uri,
                item.verdict,
                item.created,
                ))
        return self.render_to_csv(data)


class FormatReportListView(ListView):
    queryset = Report.objects.filter(report_type='format')
    template_name = 'reports/list.html'

    def get_context_data(self, **kwargs):
        context = super(FormatReportListView, self).get_context_data(**kwargs)
        context['running'] = Report.objects.filter(report_type='format', process_status='started').order_by('-start_time')
        context['queued'] = Report.objects.filter(report_type='format', process_status='queued').order_by('-start_time')
        context['completed'] = Report.objects.filter(report_type='format', process_status='completed').order_by('-end_time')
        return context


class FormatReportDataView(CSVResponseMixin, View):
    model = Report

    def get(self, request, *args, **kwargs):
        data = [('File', 'URI', 'Format', 'Time Checked',)]
        items = FormatReportItem.objects.filter(report=kwargs['pk'])
        for item in items:
            data.append((
                item.file,
                item.uri,
                item.file_format,
                item.created,
                ))
        return self.render_to_csv(data)


class FixityReportViewSet(ModelViewSet):
    model = Report
    serializer_class = FixityReportSerializer
    queryset = Report.objects.filter(report_type='fixity')

    def create(self, request):
        start_time = timezone.now()
        if 'start_time' in request.POST:
            start_time = request.POST['start_time']
        print(start_time)
        report = Report.objects.create(
            process_status="queued",
            queued_time=start_time,
            report_type='fixity',
        )
        serializer = FixityReportSerializer(report, context={'request': request})
        return Response(serializer.data)


class FormatReportViewSet(ModelViewSet):
    model = Report
    serializer_class = FormatReportSerializer
    queryset = Report.objects.filter(report_type='format')

    def create(self, request):
        start_time = timezone.now()
        if 'start_time' in request.POST:
            start_time = request.POST['start_time']
        report = Report.objects.create(
            process_status="queued",
            queued_time=start_time,
            report_type='format',
        )
        serializer = FormatReportSerializer(report, context={'request': request})
        return Response(serializer.data)


class ReportRunView(APIView):
    """Runs fixity and format reports. Accepts POST requests only."""

    def post(self, request, format=None, *args, **kwargs):
        log = logger.new(transaction_id=str(uuid4()))
        report_type = self.kwargs.get('report')
        try:
            ReportRunner().run(report_type)
            return Response({"detail": "{} reports complete.".format(report_type)}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
