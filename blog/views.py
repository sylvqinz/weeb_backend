from rest_framework import permissions, generics
from .models import Article
from .serializers import ArticleSerializer

# Vue pour récupérer tous les articles (GET)
class ArticleListView(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]

# Vue pour accéder à un article en particulier (GET)
class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'
