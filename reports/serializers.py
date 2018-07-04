from rest_framework import serializers
from reports.models import FixityReport, FormatReport, FixityReportItem, FormatReportItem


class FixityReportItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FixityReportItem
        fields = '__all__'


class FixityReportSerializer(serializers.HyperlinkedModelSerializer):
    errors = FixityReportItemSerializer(source="report", many=True)

    class Meta:
        model = FixityReport
        fields = ('url', 'start_time', 'end_time', 'process_status', 'items_checked', 'errors')


class FormatReportItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FormatReportItem
        fields = '__all__'


class FormatReportSerializer(serializers.HyperlinkedModelSerializer):
    files = FormatReportItemSerializer(source="report", many=True)

    class Meta:
        model = FormatReport
        fields = ('url', 'start_time', 'end_time', 'process_status', 'items_checked', 'files')
