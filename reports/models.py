from django.db import models


class Report(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    PROCESS_STATUS_CHOICES = (
        ("queued", "Report queued"),
        ("started", "Report started"),
        ("completed", "Report completed"),
    )
    process_status = models.CharField(choices=PROCESS_STATUS_CHOICES, max_length=100)
    items_checked = models.PositiveIntegerField(default=0)


class ReportItem(models.Model):
    file = models.CharField(max_length=512)
    uri = models.CharField(max_length=512)
    created = models.DateTimeField(auto_now_add=True)


class FixityReport(Report):

    def run(self):
        print("Running {}".format(self))
        # get each file
        # calculate checksum and compare to stored checksum
        # if the checksums don't match, create a report item
        # increment items_checked


class FixityReportItem(models.Model):
    report = models.ForeignKey(FixityReport, on_delete=models.CASCADE, related_name="report")
    stored_checksum = models.CharField(max_length=512)
    calculated_checksum = models.CharField(max_length=512)


class FormatReport(Report):

    def run(self):
        print("Running {}".format(self))
        # get each file
        # get format and uri
        # create report item
        # increment items checked


class FormatReportItem(models.Model):
    report = models.ForeignKey(FormatReport, on_delete=models.CASCADE, related_name="report")
    file_format = models.CharField(max_length=256)
