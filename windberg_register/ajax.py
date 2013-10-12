import json
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import datetime
from windberg_register.models import Start, Club


@dajaxice_register
def lookup_starts(request, birth, gender):
    dajax = Dajax()
    birth_date = datetime.datetime.strptime(birth, "%d.%M.%Y")

    starts = Start.for_birth(birth_date=birth_date, gender=gender)
    starts_ids = [start.pk for start in starts]

    dajax.script('change_id_runs([%s]);' % ", ".join([str(id) for id in starts_ids]))
    return dajax.json()


@dajaxice_register
def complete_clubs(request, query):
    names = Club.objects.filter(name__icontains=query).values("name")[:10]
    return json.dumps([x["name"] for x in names])