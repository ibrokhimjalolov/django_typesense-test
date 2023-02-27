import coreapi
import coreschema
from django.core.exceptions import BadRequest
from django.utils.encoding import force_str
from rest_framework.filters import SearchFilter, BaseFilterBackend


class TsSearchBackend(SearchFilter):

    def get_ts_search_schema(self, view) -> dict:
        ts_search_schema = {
            'q': view.request.GET.get('search', ''),
            'query_by': ', '.join(view.search_fields),
        }
        return ts_search_schema


class TsFilterBackend(BaseFilterBackend):
    query_template = {
        'lte': '%s:<=%s',
        'lt': '%s:<%s',
        'gte': '%s:>=%s',
        'gt': '%s:>%s',
        'eq': '%s:=%s',
        'neq': '%s:!=%s',
        'int__in': '%s: [%s..%s]',
    }

    def _get_field_name(self, field, query):
        return f'{field}__{query}'

    def get_ts_search_schema(self, view) -> dict:
        filter_by_values = []
        for field in view.filter_fields:
            queries = view.filter_fields[field]
            for query in queries:
                if view.request.GET.get(self._get_field_name(field, query), ''):
                    try:
                        filter_by_values.append(self.query_template[query] % (
                            field, *view.request.GET.get(self._get_field_name(field, query), '').split('__')
                        ))
                    except TypeError:
                        raise BadRequest(f'Invalid query for {field}__{query}')
        return {'filter_by': ' && '.join(filter_by_values)}

    def get_schema_fields(self, view):
        schemas = []
        for field in view.filter_fields:
            queries = view.filter_fields[field]
            for query in queries:
                field_name = f'{field}__{query}'
                schemas.append(
                    coreapi.Field(
                        name=field_name,
                        required=False,
                        location='query',
                        schema=coreschema.String(
                            title=force_str(field_name),
                            description=force_str(field_name)
                        )
                    )
                )
        return schemas

    def get_schema_operation_parameters(self, view):
        return []
