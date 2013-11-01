from cms.app_base import CMSApp
from django.utils.translation import ugettext_lazy as _
from cms.apphook_pool import apphook_pool


class WindbergResultApp(CMSApp):
    name = _('Result App')
    urls = ['windberg_results.urls']


apphook_pool.register(WindbergResultApp)