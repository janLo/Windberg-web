import codecs
from collections import defaultdict
from django.http import HttpResponse
import unicodecsv
from windberg_register import models
from django.contrib import admin


class StarterAdmin(admin.ModelAdmin):
    list_display = ("name", "given", "age_group_short", "club_name", "email", "run_list", "comment")
    list_per_page = 1000
    actions = ['_make_csv_list']

    def club_name(self, obj):
        return obj.club.name
    club_name.short_description = u"Verein"

    def age_group_short(self, obj):
        return obj.actual_age_group().short
    age_group_short.short_description = u"gemeldete Ak"

    def run_list(self, obj):
        return u"; ".join(r.name for r in obj.runs.all())
    run_list.short_description = u"gemeldete Wertungen"

    def _make_csv_list(self, request, queryset):
        run_dict = defaultdict(list)
        for starter in queryset:
            for run in starter.runs.all():
                run_dict[run.name].append(starter)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="meldungen.csv"'

        writer = unicodecsv.writer(response)

        for collected_run in run_dict:
            writer.writerow([collected_run])
            for starter in run_dict[collected_run]:
                writer.writerow(["", "", "", starter.name, starter.given, starter.birth.year, starter.club.name,
                                 starter.actual_age_group().short])
            writer.writerow([""])
        return response
    _make_csv_list.short_description = "export CSV"


admin.site.register(models.AgeGroup)
admin.site.register(models.Club)
admin.site.register(models.Run)
admin.site.register(models.Start)
admin.site.register(models.Starter, StarterAdmin)
admin.site.register(models.Version)
