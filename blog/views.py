from rest_framework.response import Response
from rest_framework.views import APIView


class PostExtraFilterView(APIView):
    
    def get(self, request):
        from .documents import PostCollection
        collection = PostCollection.get_collection()
        print(collection)
        
        data = collection.documents.search({"q": "", "query_by": "title"})
        print(data)
        return Response(data)
