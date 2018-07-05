# Generated by Django 2.0 on 2018-07-05 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FixityReportItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stored_checksum', models.CharField(max_length=512)),
                ('calculated_checksum', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='FormatReportItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_format', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
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
            name='FixityReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.Report')),
            ],
            bases=('reports.report',),
        ),
        migrations.CreateModel(
            name='FormatReport',
            fields=[
                ('report_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='reports.Report')),
            ],
            bases=('reports.report',),
        ),
        migrations.AddField(
            model_name='formatreportitem',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='reports.FormatReport'),
        ),
        migrations.AddField(
            model_name='fixityreportitem',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report', to='reports.FixityReport'),
        ),
    ]
