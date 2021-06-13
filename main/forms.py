from django import forms

from .models import *


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('created', 'user')
        # fields = '__all__'


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)