from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from windberg_register.models import Start, Version


class StartsTablePlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Starts Table")
    render_template = "register/start_table.html"

    def render(self, context, instance, placeholder):
        version = Version.current_active()
        if version is None:
            context['starts'] = []
        else:
            context['starts'] = version.starts.order_by('start_time').all()
        return context

plugin_pool.register_plugin(StartsTablePlugin)


