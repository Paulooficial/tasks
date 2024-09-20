from django.db import models
from django.conf import settings  # Para acessar o modelo de User

class Author(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=20, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    about = models.TextField(blank=True)
    fans_count = models.IntegerField(default=0)
    ratings_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    text_reviews_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Book(models.Model):
    book_id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    published_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'book')  # Garante que o usuário não favorite o mesmo livro mais de uma vez

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

