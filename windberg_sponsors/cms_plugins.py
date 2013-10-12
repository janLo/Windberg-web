from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _
from windberg_sponsors.models import CategoryPlugin, SponsorCategory, Sponsor


class SponsorStartpageCategoryPlugin(CMSPluginBase):
    model = CategoryPlugin
    name = _("Sponsor Category (Starttage)")
    render_template = "windberg_sponsors/start_page.html"

    def render(self, context, instance, placeholder):
        sponsors = Sponsor.objects.filter(category=instance.category).all()
        context['sponsors'] = sponsors
        return context


plugin_pool.register_plugin(SponsorStartpageCategoryPlugin)

class SponsorFooterImportantPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("Sponsor Important (Footer)")
    render_template = "windberg_sponsors/sponsor_footer.html"

    def render(self, context, instance, placeholder):
        sponsors = Sponsor.objects.filter(category__important=True).all()
        context['sponsors'] = sponsors
        return context


plugin_pool.register_plugin(SponsorFooterImportantPlugin)