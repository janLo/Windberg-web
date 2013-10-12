# coding=utf-8
from itertools import chain
from bootstrap3_datetime.widgets import DateTimePicker
from django.forms import SelectMultiple, CheckboxInput, ModelMultipleChoiceField, TextInput
from django.utils.encoding import force_text, smart_text
from django.utils.html import format_html_join, format_html
from django.utils.safestring import mark_safe


_table_header = """
<table class="table table-striped table-condensed" id="select_table_%(name)s">
    <thead>
    <tr>
        <th>Teilnahme</th>
        <th>Startzeit</th>
        <th>Strecke</th>
        <th>Beschreibung</th>
    </tr>
    </thead>
    <tbody>
"""

_table_footer = """
    </tbody>
</table>
"""

_check_js = "<script>" + """
$().ready(function(){

  $('input.%(class)s').prettyCheckable({
    color: 'green'
  });

});

function change_%(name)s ( enabled_ids ) {
    var $tbody = $("#select_table_%(name)s").find("tbody");
    if (enabled_ids.length == 0) {
        $tbody.find("tr.lastline").show(200);
    } else {
        $tbody.find("tr.lastline").hide(300);
    }
    $tbody.find("tr.entry").each(function(idx, elem) {
        var $elem = $(elem);
        var hidden = $elem.is(":hidden");
        var $input = $elem.find("input");
        var value =  parseInt($input.val());

         var enabled = $.inArray(value, enabled_ids) != -1;

        var clickedParent = $input.closest('.clearfix');
        var fakeCheckable = $(clickedParent).find('a');

        if (!enabled) {
            if (!hidden) {
                $elem.hide(300);
            }
            $input.prop("checked", false);
            fakeCheckable.removeClass('checked');
        } else {
            if (hidden) {
                 $elem.show(200);
            }
        }
    })
}
</script>
"""


class TableSelectMultiple(SelectMultiple):
    class Media:
        class _js_files(object):
            def __iter__(self):
                yield "pretty_checkable/prettyCheckable.js"

        js = _js_files()
        css = {'all': ('pretty_checkable/prettyCheckable.css',), }

    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [_table_header % {"name": attrs["id"]}]
        # Normalize to strings
        str_values = set([force_text(v) for v in value])

        extra_class = "check_%s" % attrs["id"]
        if "class" in final_attrs:
            final_attrs["class"] = "%s %s" % (final_attrs["class"], extra_class)
        else:
            final_attrs["class"] = extra_class

        for i, (option_value, option_object) in enumerate(chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = format_html(' for="{0}"', final_attrs['id'])
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
            option_value = force_text(option_value)
            rendered_cb = cb.render(name, option_value)
            distance = "0 m"
            description = "?"
            if len(option_object.runs.all()):
                distances = list(set([run.distance for run in option_object.runs.all()]))
                distance = ", ".join(["%d m" % d for d in distances])
                description = "; ".join(run.name for run in option_object.runs.all())
            distance = force_text(distance)
            description = smart_text(description)

            tr_id = "select_line_%s" % final_attrs["id"]
            output.append(
                format_html(
                    u'<tr id="{5}" class="entry"><td>{0}</td><td>{1}</td><td><label{2}>{3}</label></td><td>{4}</td></tr>',
                    rendered_cb,
                    force_text(option_object.start_time),
                    label_for,
                    distance,
                    description,
                    tr_id))
        output.append(format_html(
            u'<tr class="lastline"><td colspan="4" class="alert alert-success">bitte erst oben ausfüllen</td></tr>'))
        output.append(_table_footer)
        output.append(_check_js % {"name": attrs["id"], "class": extra_class})
        return mark_safe('\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_


class StartChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj


_event_js = """<script>
    $(function () {
        var $input = $("#%s");
        $input.closest("div.date").on("changeDate", function (ev) {
            %s($(this).data("datetimepicker").formatDate(ev.date));
        })
    });
</script>"""


class EventedDateTimePicker(DateTimePicker):
    def __init__(self, attrs=None, format=None, options=None, div_attrs=None, on_change=None):
        if not div_attrs: div_attrs = {'class': 'input-group date'}
        super(EventedDateTimePicker, self).__init__(attrs, format, options, div_attrs)

        self.on_change = on_change

    def render(self, name, value, attrs=None):
        output = super(EventedDateTimePicker, self).render(name, value, attrs)

        if self.on_change is not None:
            output = output + mark_safe(force_text(_event_js % (attrs["id"], self.on_change)))

        return output


_completer_js = "<script>" + """
$().ready(function(){
    $('#%(field_id)s').typeahead({
        source: function(query, process) {
            if (query.length < 2)
                return;
            Dajaxice.%(dajax_endpoint)s(process,{'query':query})
        }
    })
});
""" + "</script>"


class CompleterWidget(TextInput):
    class Media:
        class _js_files(object):
            def __iter__(self):
                yield "js/bootstrap3-typeahead.min.js"

        js = _js_files()

    def __init__(self, attrs=None, dajax_endpoint=None):
        super(CompleterWidget, self).__init__()
        self.dajax_endpoint = dajax_endpoint

    def render(self, name, value, attrs=None):
        js = _completer_js % {"field_id": attrs["id"],
                              "dajax_endpoint": self.dajax_endpoint}
        field = super(CompleterWidget, self).render(name, value, attrs)
        return field + mark_safe(js)


