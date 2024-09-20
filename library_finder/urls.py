
from django.contrib import admin
from django.urls import path, include
from books.views import register_user, login_user
from books import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/authors/', views.AuthorViewSet.as_view({'get': 'list'})),  # Lista de autores
    path('api/books/', views.BookViewSet.as_view({'get': 'list'})),  # Lista de livros
    path('register/', views.register_user, name='register'),  # Rota para registro de usuário
    path('login/', views.login_user, name='login'),  # Rota para login de usuário
    path('api/add_favorite/<int:book_id>/', views.add_favorite, name='add_favorite'),  # Adicionar favorito
    path('api/remove_favorite/<int:book_id>/', views.remove_favorite, name='remove_favorite'),  # Remover favorito
    path('api/recommend/', views.recommend_books, name='recommend_books'),  # Recomendação de livros
]

