from windberg_register import models
from django.contrib import admin


class StarterAdmin(admin.ModelAdmin):
    list_display = ("name", "given", "age_group_short", "club_name", "email", "run_list", "comment")
    list_per_page = 1000

    def club_name(self, obj):
        return obj.club.name
    club_name.short_description = u"Verein"

    def age_group_short(self, obj):
        return obj.actual_age_group().short
    age_group_short.short_description = u"gemeldete Ak"

    def run_list(self, obj):
        return  u"; ".join(r.name for r in obj.runs.all())
    run_list.short_description = u"gemeldete Wertungen"



admin.site.register(models.AgeGroup)
admin.site.register(models.Club)
admin.site.register(models.Run)
admin.site.register(models.Start)
admin.site.register(models.Starter, StarterAdmin)
admin.site.register(models.Version)
