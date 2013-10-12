from cms.app_base import CMSApp
from django.utils.translation import ugettext_lazy as _
from cms.apphook_pool import apphook_pool


class WindbergRegistrationApp(CMSApp):
    name = _('Registration App')
    urls = ['windberg_register.urls']


apphook_pool.register(WindbergRegistrationApp)