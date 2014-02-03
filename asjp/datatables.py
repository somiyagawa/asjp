import re

from sqlalchemy import or_
from clld.web.datatables import Values
from clld.web.datatables.base import (
    Col, LinkCol, LinkToMapCol, IntegerIdCol,
)
from clld.web.datatables.language import Languages
from clld.db.models.common import Language, Parameter, Value

from asjp.models import Doculect, Word


class Words(Values):
    """Lists of words
    """
    def col_defs(self):
        if self.parameter:
            res = [
                LinkCol(
                    self, 'language',
                    model_col=Language.name,
                    get_object=lambda i: i.valueset.language),
            ]
        elif self.contribution:
            res = [
                LinkCol(
                    self, 'meaning',
                    model_col=Parameter.name,
                    get_object=lambda i: i.valueset.parameter),
            ]
        elif self.language:
            res = [
                IntegerIdCol(
                    self, 'id',
                    input_size='mini',
                    model_col=Parameter.id,
                    get_object=lambda i: i.valueset.parameter),
                LinkCol(
                    self, 'meaning',
                    model_col=Parameter.name,
                    get_object=lambda i: i.valueset.parameter),
            ]
        else:
            res = []
        return res + [
            Col(self, 'name', sTitle='Word', model_col=Value.name),
            Col(self, 'loan', model_col=Word.loan),
        ]


class IsoCol(Col):
    __kw__ = dict(sTitle='ISO 639-3', input_size='mini')

    def search(self, qs):
        whitespace = re.compile('\s+')
        if whitespace.search(qs):
            return or_(*[
                Doculect.code_iso == q.strip() for q in whitespace.split(qs.lower())])
        return Col.search(self, qs)


class Wordlists(Languages):
    def col_defs(self):
        return [
            LinkToMapCol(self, 'm'),
            LinkCol(self, 'name'),
            Col(self, 'glottocode', model_col=Doculect.code_glottolog),
            IsoCol(self, 'iso', model_col=Doculect.code_iso),
            Col(self, 'wals', sTitle='WALS', input_size='mini', model_col=Doculect.code_wals),
            Col(self, 'latitude', input_size='mini'),
            Col(self, 'longitude', input_size='mini'),
            Col(self, 'number_of_speakers', model_col=Doculect.number_of_speakers),
            Col(self, 'long_extinct', input_size='mini', model_col=Doculect.long_extinct),
            Col(self, 'recently_extinct', input_size='mini', model_col=Doculect.recently_extinct),
            Col(self, 'year_of_extinction', input_size='mini', model_col=Doculect.year_of_extinction),
            Col(self, 'classification_wals', model_col=Doculect.classification_wals),
            Col(self, 'classification_ethnologue', model_col=Doculect.classification_ethnologue),
            Col(self, 'classification_glottolog', model_col=Doculect.classification_glottolog),
        ]


def includeme(config):
    config.register_datatable('values', Words)
    config.register_datatable('languages', Wordlists)
    #config.register_datatable('contributors', Compilers)
    #config.register_datatable('contributions', Vocabularies)
    #config.register_datatable('parameters', Entries)
    #config.register_datatable('chapters', Chapters)
