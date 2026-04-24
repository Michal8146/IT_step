from django.db import models
from django.contrib.auth.models import User

    
class Category(models.Model):
    name = models.CharField(max_length=50)
    color_class = models.CharField(max_length=50, help_text="Např. text-bg-success")

    class Meta:
        verbose_name_plural = "Categories" # Zde definujeme správné množné číslo

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    excerpt = models.CharField(max_length=300)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True)


    def __str__(self):
        return self.title