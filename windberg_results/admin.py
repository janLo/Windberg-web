from functools import update_wrapper
from django.conf.urls import patterns, url
from django.contrib import admin
from windberg_results import models
from windberg_results.views import import_entries_from_csv


class ResultEntryInlineAdmin(admin.TabularInline):
    model = models.ResultEntry
    extra = 0


class ResultTableAdmin(admin.ModelAdmin):
    model = models.ResultTable
    inlines = [ResultEntryInlineAdmin]
    list_display = ("_version_name", "start_time", "name", "use_age_group", "use_gender")
    prepopulated_fields = {"slug": ("name",)}

    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urls = super(ResultTableAdmin, self).get_urls()
        my_urls = patterns('',
                           url(r'^(?P<year>\d{4})/(?P<slug>[-\w]+)/import/$',
                               wrap(import_entries_from_csv), name="import_result_csv"),
        )
        return my_urls + urls

    def _version_name(self, obj):
        return u"%d. (%d)" % (obj.version.number, obj.version.date.year)

    _version_name.short_description = u"Auflage"


admin.site.register(models.ResultTable, ResultTableAdmin)
