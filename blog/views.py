from django_typesense.filter_backends import TsSearchBackend, TsFilterBackend
from django_typesense.views import TsSearchFilterView
from .documents import PostDocument
from .models import Post
from .serializers import PostSerializer


class PostExtraFilterView(TsSearchFilterView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    document = PostDocument
    filter_backends = [TsSearchBackend, TsFilterBackend]
    search_fields = ['title', 'body']
    filter_fields = {
        'number': ['lte', 'gte', 'eq', 'neq', 'int__in'],
    }
