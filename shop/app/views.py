from django.shortcuts import render
from django.db.models import Count
from urllib import request
from django.views import View
from . models import Product, Heading, Category

# Create your views here.
def home(request):
    headings = Heading.objects.all()
    heading_category_map = {}
    for heading in headings:
        heading_category_map[heading.heading_name] = Category.objects.filter(heading=heading)
    return render(request,"app/home.html", {'heading_category_map' : heading_category_map})

class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        subcategory = Product.objects.filter(category=val).values('subcategory').annotate(total=Count('subcategory'))
        return render(request, "app/category.html", locals())