from datetime import datetime

from django_cron import CronJobBase, Schedule

from reports.models import FixityReport, FormatReport


class RunReports(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'transfers.discover_transfers'

    def do(self):
        current_time = datetime.now()
        for report_type in [
            FixityReport.objects.filter(process_status='queued', start_time__lte=current_time),
            FormatReport.objects.filter(process_status='queued', start_time__lte=current_time)
        ]:
            for report in report_type:
                report.run()
