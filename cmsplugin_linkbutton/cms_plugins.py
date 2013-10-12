from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.plugins.link.cms_plugins import LinkPlugin
from cms.plugins.link.forms import LinkForm
from cms.plugins.link.models import Link
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class LinkButtonPlugin(LinkPlugin):
    model = Link
    form = LinkForm
    name = _("Link Button")
    render_template = "link_button/link_button.html"


    def icon_src(self, instance):
        return settings.STATIC_URL + u"link_button/images/button.png"

plugin_pool.register_plugin(LinkButtonPlugin)