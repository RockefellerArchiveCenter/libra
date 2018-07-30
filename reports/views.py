from datetime import datetime
import logging
from structlog import wrap_logger
from uuid import uuid4

from django.shortcuts import render
from django.views.generic import ListView, TemplateView, View

from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from reports.formatmixins import CSVResponseMixin
from reports.models import FixityReport, FixityReportItem, FormatReport, FormatReportItem
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
        context['fixity_reports']['objects'] = FixityReport.objects.all()
        context['fixity_reports']['running'] = FixityReport.objects.filter(process_status='started').count()
        context['fixity_reports']['queued'] = FixityReport.objects.filter(process_status='queued').count()
        context['fixity_reports']['completed'] = FixityReport.objects.filter(process_status='completed').count()
        context['format_reports']['objects'] = FormatReport.objects.all()
        context['format_reports']['running'] = FormatReport.objects.filter(process_status='started').count()
        context['format_reports']['queued'] = FormatReport.objects.filter(process_status='queued').count()
        context['format_reports']['completed'] = FormatReport.objects.filter(process_status='completed').count()
        return context


class FixityReportListView(ListView):
    queryset = FixityReport.objects.all()
    template_name = 'reports/list.html'

    def get_context_data(self, **kwargs):
        context = super(FixityReportListView, self).get_context_data(**kwargs)
        context['running'] = FixityReport.objects.filter(process_status='started').order_by('-start_time')
        context['queued'] = FixityReport.objects.filter(process_status='queued').order_by('-start_time')
        context['completed'] = FixityReport.objects.filter(process_status='completed').order_by('-end_time')
        return context


class FixityReportDataView(CSVResponseMixin, View):
    model = FixityReport

    def get(self, request, *args, **kwargs):
        data = [('File', 'URI', 'Stored Checksum', 'Calculated Checksum', 'Time Checked',)]
        items = FixityReportItem.objects.filter(report=kwargs['pk'])
        print(items)
        for item in items:
            data.append((
                item.file,
                item.uri,
                item.stored_checksum,
                item.calculated_checksum,
                item.created,
                ))
        return self.render_to_csv(data)


class FormatReportListView(ListView):
    queryset = FormatReport.objects.all()
    template_name = 'reports/list.html'

    def get_context_data(self, **kwargs):
        context = super(FormatReportListView, self).get_context_data(**kwargs)
        context['running'] = FormatReport.objects.filter(process_status='started').order_by('-start_time')
        context['queued'] = FormatReport.objects.filter(process_status='queued').order_by('-start_time')
        context['completed'] = FormatReport.objects.filter(process_status='completed').order_by('-end_time')
        return context


class FormatReportDataView(CSVResponseMixin, View):
    model = FormatReport

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


class FixityReportViewSet(viewsets.ModelViewSet):
    model = FixityReport
    serializer_class = FixityReportSerializer
    queryset = FixityReport.objects.all()

    def create(self, request):
        start_time = datetime.now()
        if 'start_time' in request.POST:
            start_time = request.POST['start_time']
        report = FixityReport.objects.create(
            process_status="queued",
            start_time=start_time,
        )
        serializer = FixityReportSerializer(report, context={'request': request})
        return Response(serializer.data)


class FormatReportViewSet(viewsets.ModelViewSet):
    model = FormatReport
    serializer_class = FormatReportSerializer
    queryset = FormatReport.objects.all()

    def create(self, request):
        start_time = datetime.now()
        if 'start_time' in request.POST:
            start_time = request.POST['start_time']
        report = FormatReport.objects.create(
            process_status="queued",
            start_time=start_time,
        )
        else:
            report = FormatReport.objects.create(
                process_status="started",
                start_time=datetime.now(),
            )
        serializer = FormatReportSerializer(report, context={'request': request})
        return Response(serializer.data)
