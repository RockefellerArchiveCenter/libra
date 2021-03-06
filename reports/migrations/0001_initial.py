# Generated by Django 2.0.8 on 2018-10-11 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('queued_time', models.DateTimeField(blank=True, null=True)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('report_type', models.CharField(choices=[('fixity', 'Fixity'), ('format', 'Format')], max_length=100)),
                ('process_status', models.CharField(choices=[('queued', 'Report queued'), ('started', 'Report started'), ('completed', 'Report completed')], max_length=100)),
                ('items_checked', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ReportItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.CharField(max_length=512)),
                ('uri', models.CharField(max_length=512)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FixityReportItem',
            fields=[
                ('reportitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.ReportItem')),
                ('verdict', models.CharField(max_length=10)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixity_report', to='reports.Report')),
            ],
            bases=('reports.reportitem',),
        ),
        migrations.CreateModel(
            name='FormatReportItem',
            fields=[
                ('reportitem_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.ReportItem')),
                ('file_format', models.CharField(max_length=256)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='format_report', to='reports.Report')),
            ],
            bases=('reports.reportitem',),
        ),
    ]
