# Create your views here.o
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import reverse
from django.db import transaction

from django.db.models.aggregates import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import RedirectView, ListView, DetailView
import models
from windberg_register.models import Version
from windberg_results import forms
from windberg_results.result_import import UploadedResultFile


class ResultListingRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self):
        version = Version.objects.values("date").annotate(result_tables=Count("resulttable__id")).filter(
            result_tables__gt=0).order_by('-date')
        if not version:
            return reverse("windberg_no_results")

        return reverse("windberg_version_results", kwargs={"year": version[0]["date"].year})


class VersionBasedViewMixin(object):
    def retrieve_version(self):
        self.year = int(self.kwargs["year"])
        self.version = Version.by_year(self.year)
        if not self.version:
            raise Http404
        return self.version


class ResultTableListView(ListView, VersionBasedViewMixin):
    template_name = "results/result_table_list.html"

    def get_queryset(self):
        self.retrieve_version()
        return models.ResultTable.objects.filter(version=self.version).select_related("entries").order_by("start_time")

    def get_context_data(self, **kwargs):
        context = super(ResultTableListView, self).get_context_data(**kwargs)
        context["version"] = self.version
        prev_version = Version.objects.filter(date__lt=self.version.date, resulttables__isnull=False).order_by("-date")
        if prev_version.count() > 0:
            context["prev"] = prev_version.all()[0]
        next_version = Version.objects.filter(date__gt=self.version.date, resulttables__isnull=False).order_by("date")
        if next_version.count() > 0:
            context["next"] = next_version.all()[0]

        return context


class ResultTableDefaultView(DetailView, VersionBasedViewMixin):
    template_name = "results/result_table_detail.html"

    def get_queryset(self):
        self.retrieve_version()
        return models.ResultTable.objects.filter(slug=self.kwargs["slug"]).select_related("entries")

    def get_context_data(self, **kwargs):
        context = super(ResultTableDefaultView, self).get_context_data(**kwargs)
        context["version"] = self.version
        return context

from pprint import pprint

@staff_member_required
def import_entries_from_csv(request, year, slug):
    version = Version.by_year(int(year))
    if not version:
        raise Http404

    table = get_object_or_404(models.ResultTable, version=version, slug=slug)

    if request.method == "POST":
        form = forms.CsvImportForm(request.POST, request.FILES)
        print "peng"
        if form.is_valid():
            with UploadedResultFile(request.FILES["import_file"]) as import_file:
                with transaction.commit_on_success():
                    for entry in import_file:
                        pprint(entry)
                        models.ResultEntry.objects.create(table=table, **entry)

            return redirect('admin:windberg_results_resulttable_change', table.id )
        print form.errors
    else:
        form = forms.CsvImportForm({"resulttable": table.id})

    return render(request, "admin/windberg_results/upload_form.html",  {'form': form})