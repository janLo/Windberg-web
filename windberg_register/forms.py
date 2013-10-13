# vim: set encoding=utf8
from bootstrap3_datetime.widgets import DateTimePicker

from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput
from windberg_register.models import Version, Club, Starter, AgeGroup, Run, Start
from windberg_register.widgets import TableSelectMultiple, StartChoiceField, EventedDateTimePicker, CompleterWidget


class PreSelectField(forms.CharField):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model")
        super(PreSelectField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned = super(PreSelectField, self).clean(*args, **kwargs)
        return self.model.get_or_create(cleaned)


def run_queryset():
    version = Version.current_active()
    if version:
        return version.starts
    return None


class AppointmentForm(forms.ModelForm):
    club = PreSelectField(model=Club, max_length=30, label=u"Verein",
                          widget=CompleterWidget(dajax_endpoint="windberg_register.complete_clubs"))
    runs = StartChoiceField(queryset=run_queryset(), widget=TableSelectMultiple, label="Starts")
    birth = forms.DateField(input_formats=("%d.%M.%Y",),
                            label="Geburtstag",
                            widget=EventedDateTimePicker(
                                options={"format": "dd.MM.yyyy", "pickTime": True, 'viewMode': 2,
                                         "minViewMode": "days"},
                                attrs={"readonly": True, }, on_change="update_starts"))
    email = forms.EmailField()
    comment = forms.CharField(label="Anmerkungen", widget=forms.Textarea(attrs={"rows": "3"}),
                              required=False)

    class Meta:
        model = Starter
        exclude = ("version",)
        fields = ['name', 'given', 'gender', 'birth', 'club', 'email', 'runs', 'comment']

    def clean(self):
        cleaned = super(AppointmentForm, self).clean()

        for needed in ("birth", "gender", "runs"):
            if needed not in cleaned:
                return cleaned


        possible_starts = Start.for_birth(cleaned["birth"], cleaned["gender"])

        for run in cleaned["runs"]:
            if run not in possible_starts:
                raise ValidationError("Gewählte Läufe passen nicht zu Ihrer Altersklasse")
        ages = AgeGroup.select_from_birth(cleaned["birth"], cleaned["gender"])
        starts = Run.objects.filter(start__in=cleaned["runs"]).filter(possible_ages__in=ages)
        if not starts.count():
            raise ValidationError("Gewählte Läufe passen nicht zu Ihrer Altersklasse")
        cleaned["runs"] = starts

        return cleaned
