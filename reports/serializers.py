from rest_framework import serializers
from reports.models import FixityReport, FormatReport


class FixityReportSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FixityReport
        fields = '__all__'


class FormatReportSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FormatReport
        fields = '__all__'
