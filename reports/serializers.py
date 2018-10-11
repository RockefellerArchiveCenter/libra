from rest_framework import serializers
from reports.models import Report, FixityReportItem, FormatReportItem
from django.urls import reverse


class FixityReportSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Report
        fields = ('url', 'report_type', 'created_time', 'start_time', 'end_time', 'process_status', 'items_checked',)
        extra_kwargs = {'url': {'view_name': 'fixityreport-detail'}}


class FormatReportSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Report
        fields = ('url', 'created_time', 'start_time', 'end_time', 'process_status', 'items_checked',)
        extra_kwargs = {'url': {'view_name': 'formatreport-detail'}}


class FormatReportItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FormatReportItem
        fields = '__all__'


class FixityReportItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FixityReportItem
        fields = '__all__'
