from django.db import models


class Report(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    PROCESS_STATUS_CHOICES = (
        ("queued", "Report queued"),
        ("started", "Report started"),
        ("completed", "Report completed"),
    )
    process_status = models.CharField(choices=PROCESS_STATUS_CHOICES, max_length=100)


class FixityReport(Report):

    def run(self):
        print("Running {}".format(self))


class FormatReport(Report):

    def run(self):
        print("Running {}".format(self))
