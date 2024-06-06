from django.shortcuts import render
from django.db.models import Count
from urllib import request
from django.views import View
from . models import Product

# Create your views here.
def home(request):
    return render(request,"app/home.html")

class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        subcategory = Product.objects.filter(category=val).values('subcategory').annotate(total=Count('subcategory'))
        return render(request, "app/category.html", locals())