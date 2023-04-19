from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .document import TypesenseDocument
from .paginators import FacetsPageNumberPagination


class TsSearchFilterView(ListAPIView):
    search_fields = []
    document = TypesenseDocument
    pagination_class = FacetsPageNumberPagination

    def filter_queryset(self, queryset):
        ts_search_schema = {}
        for filter_backend in self.filter_backends:
            ts_search_schema = {**ts_search_schema, **(filter_backend().get_ts_search_schema(self))}
        ts_search_schema['page'] = int(self.request.GET.get('page', 1))
        ts_search_schema['per_page'] = int(self.request.GET.get('page_size', 10))
        ts_search_schema['facet_by'] = self.request.GET.get('facet_by', '')
        ts_search_schema['sort_by'] = self.request.GET.get('sort_by', '')
        hits = self.document.search(ts_search_schema)
        self._facets = hits['facet_counts']
        ids = [hit['document']['id'] for hit in hits['hits']]
        queryset = queryset.filter(id__in=ids)
        queryset = sorted(queryset, key=lambda x: ids.index(str(x.pk)))
        return queryset

    def get_paginated_response(self, data):
        return self.paginator.get_paginated_response(data, facets=self._facets)
