from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['book_id', 'title', 'description', 'published_date', 'author']

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = [
            'id', 'name', 'gender', 'image_url', 'about', 
            'fans_count', 'ratings_count', 'average_rating', 
            'text_reviews_count', 'books'
        ]
