from django import forms


class CsvImportForm(forms.Form):
    import_file = forms.FileField(label=u"Meldungsdatei", allow_empty_file=False)
    resulttable = forms.IntegerField(widget=forms.HiddenInput, required=True)

