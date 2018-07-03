from datetime import datetime
import logging
from structlog import wrap_logger
from uuid import uuid4

from django.shortcuts import render
from django.views.generic import View

from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from reports.models import FixityReport, FormatReport
from reports.serializers import FixityReportSerializer, FormatReportSerializer

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger = wrap_logger(logger)


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'reports/main.html')


class FixityReportViewSet(viewsets.ModelViewSet):
    model = FixityReport
    serializer_class = FixityReportSerializer
    queryset = FixityReport.objects.all()

    def create(self, request):
        report = FixityReport.objects.create(
            process_status="queued"
        )
        serializer = FixityReportSerializer(report, context={'request': request})
        return Response(serializer.data)


class FormatReportViewSet(viewsets.ModelViewSet):
    model = FormatReport
    serializer_class = FormatReportSerializer
    queryset = FormatReport.objects.all()

    def create(self, request):
        report = FormatReport.objects.create(
            process_status="queued"
        )
        serializer = FormatReportSerializer(report, context={'request': request})
        return Response(serializer.data)
