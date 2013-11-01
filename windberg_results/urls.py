from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from windberg_results import views


urlpatterns = patterns('',
    url(r'^$', views.ResultListingRedirectView.as_view(), name='windberg_default_results'),
    url(r'^none_found$', TemplateView.as_view(template_name="results/no_results.html"),
        name='windberg_no_results'),
    url(r'^(?P<year>\d{4})/full$', views.ResultTableListView.as_view(),
        name='windberg_version_results'),
    url(r'^(?P<year>\d{4})/(?P<slug>[-\w]+)$', views.ResultTableDefaultView.as_view(),
        name='windberg_slug_results'),
    )
