# coding=utf-8
import csv
from cStringIO import StringIO
import datetime
from dateutil import parser


def _parse_time(time_string):
    parsed = parser.parse(time_string)
    return parsed.time()


def _convert_text(text):
    return unicode(text, "latin1").strip()


def _int_or_None(value):
    if value:
        return int(value)
    return None


def _rename_to(name):
    def do_rename(value):
        return [(name, value)]

    return do_rename


def _make_gender_rank_processor(gender):
    def _process_sex_rank(value):
        if value is None:
            return []
        return [("gender", gender), ("rank_sex", int(value))]

    return _process_sex_rank


def _process_name(value):
    splits = value.split(",", 1)
    if len(splits) == 0:
        parts = ["n/a", "n/a"]
    elif len(splits) == 1:
        parts = [splits[0], "n/a"]
    else:
        parts = splits
    return [("name", parts[0].strip()), ("given", parts[1].strip())]


def _make_birth_year(value):
    return [("birth_year", datetime.date(year=value, month=1, day=1))]


def _process_age_rank(value):
    if value is None:
        return []
    return [("rank_age", value)]


def _drop_value(value):
    return []


_convert_table = {u"Platz": int,
                  u"Plm": _int_or_None,
                  u"Plw": _int_or_None,
                  u"Stnr.": int,
                  u"Name,Vorname": _convert_text,
                  u"Verein": _convert_text,
                  u"GJ": int,
                  u"AK": _convert_text,
                  u"AKm": _int_or_None,
                  u"AKw": _int_or_None,
                  u"Endzeit": _parse_time,
                  u"Rückst.": _parse_time}

_map_table = {u"Platz": _rename_to("rank"),
              u"Plm": _make_gender_rank_processor("M"),
              u"Plw": _make_gender_rank_processor("W"),
              u"Stnr.": _rename_to("start_number"),
              u"Name,Vorname": _process_name,
              u"Verein": _rename_to("club"),
              u"GJ": _make_birth_year,
              u"AK": _rename_to("age_group"),
              u"AKm": _process_age_rank,
              u"AKw": _process_age_rank,
              u"Endzeit": _rename_to("result_time"),
              u"Rückst.": _drop_value}


class UploadedResultFile(object):
    def __init__(self, upload_file):
        file = StringIO()
        for chunk in upload_file.chunks():
            file.write(chunk)
        file.seek(0)
        self._file = file
        self._reader = None

    def __enter__(self):
        assert self._file is not None
        assert self._reader is None
        self._reader = csv.DictReader(self._file, delimiter=';', quoting=csv.QUOTE_NONE)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._reader = None
        self._file.close()
        self._file = None

    def __iter__(self):
        assert self._reader is not None
        return self

    def next(self):
        assert self._reader is not None
        line = self._reader.next()
        cleaned = []
        for field in line:
            if not field:
                continue
            if field not in _convert_table:
                continue
            converted = _convert_table[field](line[field])
            mapped = _map_table[field](converted)
            cleaned.extend(mapped)
        return dict(cleaned)