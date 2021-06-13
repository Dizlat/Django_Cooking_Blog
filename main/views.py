from datetime import timedelta

from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from  django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, DeleteView, CreateView

from .forms import *
from .models import *


# def index(request):
#     recipes = Recipe.objects.all()
#     return render(request, 'index.html', {'recipes': recipes})

class MainPageView(ListView):
    model = Recipe
    template_name = 'index.html'
    context_object_name = 'recipes'
    paginate_by = 2

    def get_template_names(self):
        template_name = super(MainPageView, self).get_template_names()
        search = self.request.GET.get('q')
        if search:
            template_name = 'search.html'
        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        filter = self.request.GET.get('filter')
        if search:
            context['recipes'] = Recipe.objects.filter(Q(tittle__icontains=search)|
                                                       Q(description__icontains=search))
        elif filter:
            start_date = timezone.now() - timedelta(days=1)
            context['recipes'] = Recipe.objects.filter(created__gte=start_date)
        else:
            context['recipes'] = Recipe.objects.all()
        return context


# def category_detail(request, slug):
#     category = Category.objects.get(slug=slug)
#     recipes = Recipe.objects.filter(category_id=slug)
#     return render(request, 'category-detail.html', locals())

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category-detail.html'
    context_object_name = 'category'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.slug = kwargs.get('slug', None)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.filter(category_id=self.slug)
        return context


# def recipe_detail(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)
#     image = recipe.get_image
#     images = recipe.images.exclude(id=image.id)
#     return render(request, 'recipe-detail.html', locals())

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe-detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = self.get_object().get_image
        context['images'] = self.get_object().images.exclude(id=image.id)
        return context


def add_recipe(request):   # CreateView: model, template_name, context_object_name, form_class
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if recipe_form.is_valid() and formset.is_valid():
            recipe = recipe_form.save()
            for form in formset.cleaned_data:
                image = form['image']
                Image.objects.create(image=image, recipe=recipe)
            return redirect(recipe.get_absolute_url())
    else:
        recipe_form = RecipeForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'add-recipe.html', locals())


def update_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=5)
    recipe_form = RecipeForm(request.POST or None, instance=recipe)
    formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.filter(recipe=recipe))
    if recipe_form.is_valid() and formset.is_valid():
        recipe_form.save()

        for form in formset:
            image = form.save(commit=False)
            image.recipe = recipe
            image.save()
        return redirect(recipe.get_absolute_url())
    return render(request, 'update-recipe.html', locals())


# def delete_recipe(request, pk):
#     recipe = get_object_or_404(Recipe, pk=pk)
#     if request.method == 'POST':
#         recipe.delete()
#         messages.add_message(request, messages.SUCCESS, 'Successfully deleted!')
#         return redirect('home')
#     return render(request, 'delete-recipe.html')

class DeleteRecipeView(DeleteView):
    model = Recipe
    template_name = 'delete-recipe.html'
    success_url = reverse_lazy('home')

    def delete(self, request, *args, **kwargs):

        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.add_message(request, messages.SUCCESS, 'Successfully deleted!')
        return HttpResponseRedirect(success_url)


