from django.shortcuts import render
from django.db.models import Count
from urllib import request
from django.views import View
from . models import Product, Heading, Category, SpeacialHeadingProduct, SpecialHeadng

# Create your views here.
def home(request):
    headings = Heading.objects.all()
    special_heading_list =  SpecialHeadng.objects.all()
    heading_category_map = {}
    special_heading_product_list = []
    for heading in headings:
        heading_category_map[heading.heading_name] = Category.objects.filter(heading=heading)
    for special_heading in special_heading_list:
        product_list = []
        for special_product in SpeacialHeadingProduct.objects.filter(special_heading=special_heading.pk):
            product_list.append(special_product.product)
        special_heading_product_list.append({
            "name" : special_heading.name,
            "description" : special_heading.description,
            "product_list" : product_list
        })
    print(special_heading_product_list)
    return render(request,"app/home.html", {'heading_category_map' : heading_category_map, 'special_heading_product_list' : special_heading_product_list})

class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        subcategory = Product.objects.filter(category=val).values('subcategory').annotate(total=Count('subcategory'))
        return render(request, "app/category.html", locals())