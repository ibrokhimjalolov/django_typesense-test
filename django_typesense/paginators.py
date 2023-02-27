import coreapi
import coreschema
from django.core.paginator import InvalidPage
from django.utils.encoding import force_str
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FacetsPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        """
                Paginate a queryset if required, either returning a
                page object, or `None` if pagination is not configured for this view.
                """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = 1

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_paginated_response(self, data, facets=None):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'facets': facets,
            'results': data
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?{page_query_param}=4'.format(
                        page_query_param=self.page_query_param)
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'http://api.example.org/accounts/?{page_query_param}=2'.format(
                        page_query_param=self.page_query_param)
                },
                'facets': {
                    'type': 'string',
                    'nullable': False,
                    'format': 'string',
                },
                'results': schema,
            },
        }

    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name='facet_by',
                required=False,
                location='query',
                schema=coreschema.String(
                    title='Facet by',
                    description='Facet by'
                )
            ),
            coreapi.Field(
                name='sort_by',
                required=False,
                location='query',
                schema=coreschema.String(
                    title='Sort by',
                    description='Sort by'
                )
            ),
            coreapi.Field(
                name=self.page_query_param,
                required=False,
                location='query',
                schema=coreschema.Integer(
                    title='Page',
                    description=force_str(self.page_query_description)
                )
            ),
            coreapi.Field(
                name='page_size',
                required=False,
                location='query',
                schema=coreschema.Integer(
                    title='Page size',
                    description=force_str(self.page_size_query_description)
                )
            )
        ]
        return fields
