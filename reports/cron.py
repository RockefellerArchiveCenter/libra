from django.utils import timezone

from django_cron import CronJobBase, Schedule

from reports.routines import ReportRunner


class RunReports(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'transfers.discover_transfers'

    def do(self):
        ReportRunner().run('fixity')
        ReportRunner().run('format')
