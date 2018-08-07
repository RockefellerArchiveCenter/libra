from rest_framework import serializers
from reports.models import FixityReport, FormatReport, FixityReportItem, FormatReportItem


class FixityReportItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FixityReportItem
        fields = '__all__'


class FixityReportSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FixityReport
        fields = ('url', 'created_time', 'start_time', 'end_time', 'process_status', 'items_checked',)


class FormatReportItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FormatReportItem
        fields = '__all__'


class FormatReportSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FormatReport
        fields = ('url', 'created_time', 'start_time', 'end_time', 'process_status', 'items_checked')
