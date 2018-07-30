from datetime import datetime
import logging
from structlog import wrap_logger
from uuid import uuid4

from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from reports.models import FixityReport, FormatReport
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


class FormatReportListView(ListView):
    queryset = FormatReport.objects.all()
    template_name = 'reports/list.html'

    def get_context_data(self, **kwargs):
        context = super(FormatReportListView, self).get_context_data(**kwargs)
        context['running'] = FormatReport.objects.filter(process_status='started').order_by('-start_time')
        context['queued'] = FormatReport.objects.filter(process_status='queued').order_by('-start_time')
        context['completed'] = FormatReport.objects.filter(process_status='completed').order_by('-end_time')
        return context


class FixityReportViewSet(viewsets.ModelViewSet):
    model = FixityReport
    serializer_class = FixityReportSerializer
    queryset = FixityReport.objects.all()

    def create(self, request):
        if 'start_time' in request.POST:
            report = FixityReport.objects.create(
                process_status="queued",
                start_time=request.POST['start_time'],
            )
        else:
            report = FixityReport.objects.create(
                process_status="started",
                start_time=datetime.now(),
            )
        serializer = FixityReportSerializer(report, context={'request': request})
        return Response(serializer.data)


class FormatReportViewSet(viewsets.ModelViewSet):
    model = FormatReport
    serializer_class = FormatReportSerializer
    queryset = FormatReport.objects.all()

    def create(self, request):
        if 'start_time' in request.POST:
            report = FormatReport.objects.create(
                process_status="queued",
                start_time=request.POST['start_time'],
            )
        else:
            report = FormatReport.objects.create(
                process_status="started",
                start_time=datetime.now(),
            )
        serializer = FormatReportSerializer(report, context={'request': request})
        return Response(serializer.data)
