from django.conf.urls import patterns, url

from django.views.generic import TemplateView

urlpatterns = patterns('',
                 url(r'^$', "windberg_register.views.register",
        name='windberg_register_process'),
    url(r'^success$', TemplateView.as_view(template_name="register/registration_success.html"),
        name='windberg_register_success'),
)


