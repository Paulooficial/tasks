from rest_framework import viewsets, filters
from .models import Author, Book, Favorite 
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated # protect endpoints
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]  # protect endpoints


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name']  # Define busca por título do livro e nome do autor
    permission_classes = [IsAuthenticated]  # protect endpoints

    def list(self, request, *args, **kwargs):
        
        query = request.query_params.get('search', None)
        if query:
            # Importação local para evitar dependências circulares
            self.queryset = self.queryset.filter(title__icontains=query) | self.queryset.filter(author__name__icontains=query)

        return super().list(request, *args, **kwargs)


# Registro de usuário
@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    user.save()

    return Response({'success': 'User created successfully'}, status=status.HTTP_201_CREATED)


# Login de usuário
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# add favorite
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite(request, book_id):
    user = request.user
    book = Book.objects.get(id=book_id)

    if Favorite.objects.filter(user=user).count() >= 20:
        return Response({'error': 'Você pode ter no máximo 20 livros favoritos.'}, status=400)

    favorite, created = Favorite.objects.get_or_create(user=user, book=book)
    if created:
        return Response({'success': f'Livro "{book.title}" adicionado aos favoritos!'})
    else:
        return Response({'message': 'Este livro já está nos seus favoritos.'}, status=200)


# Remover um livro da lista de favoritos
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite(request, book_id):
    user = request.user
    book = Book.objects.get(id=book_id)

    favorite = Favorite.objects.filter(user=user, book=book).first()
    if favorite:
        favorite.delete()
        return Response({'success': f'Livro "{book.title}" removido dos favoritos!'})
    else:
        return Response({'error': 'Este livro não está na sua lista de favoritos.'}, status=400)


# Recomendação baseada nos favoritos do usuário
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_books(request):
    user = request.user
    favorite_books = Favorite.objects.filter(user=user).values_list('book', flat=True)
    
    if not favorite_books:
        return Response({'message': 'Você ainda não tem livros favoritos para gerar recomendações.'}, status=200)
    
    # Recomendação de livros que não estão na lista de favoritos do usuário
    recommended_books = Book.objects.filter(~Q(id__in=favorite_books)).order_by('?')[:5]
    
    if not recommended_books:
        return Response({'message': 'Nenhum livro recomendado encontrado.'}, status=200)

    # Serializar e retornar os livros recomendados
    serializer = BookSerializer(recommended_books, many=True)
    return Response(serializer.data, status=200)
