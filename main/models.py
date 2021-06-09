from django.db import models

from account.models import User


class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories', blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> {self.name}'
        return self.name

    def get_children(self):
        if self.children:
            return self.children.all()
        return False


class Recipe(models.Model):
    tittle = models.CharField(max_length=250)
    description = models.TextField()
    cooking_time = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tittle

    @property
    def get_image(self):
        return self.images.first()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detail', kwargs={'pk': self.pk})


class Image(models.Model):
    image = models.ImageField(upload_to='recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.url
