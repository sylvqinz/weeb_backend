from django.db import models

class Article(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField()
	slug = models.SlugField(max_length=255, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # pour lier à l'utilisateur plus tard

	def __str__(self):
		return self.title
