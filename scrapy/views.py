from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
from .forms import URLaddressForm, ProductFormat
from .models import URLaddress, Page, Product
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer
from .admin import ProductResource
# Create your views here.

# url = "https://www.rebelgunworks.com.au/collections/all-shotguns"

s = HTMLSession()

def get_url(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup

def getnextpage(soup):
    page = soup.find("ul", class_="pagination-custom")
    if page:
        if not page.find("li", class_="disabled", string="→"):
            url = "https://www.rebelgunworks.com.au" + str(page.find("li", string="→").find("a")['href'])
            return url
        else:
            return
    else:
        return HttpResponse("data not found!")

def getdisclamer(url):
    soup = get_url(url)
    div = soup.find("div", class_="grid")
    if not div.find("p", class_="tab"):
        return
    dis = div.find("p", class_="tab").text
    print(dis)
    return dis

def scrap_completed(pk):
    page = get_object_or_404(Page, pk=pk)
    page.is_done = True
    page.save()
    print(page.is_done)
    return redirect("scrapy:pages", pk=page.url_address.pk)

def get_products(request, pk):
    page = get_object_or_404(Page, pk=pk)
    soup = get_url(page)
    products = soup.find("div", class_="grid-item large--four-fifths grid-border--left")
    div = products.find("div", class_="grid-uniform")
    link = div.find_all("a", class_="product-grid-item")
    for n in link:
        dis = getdisclamer("https://www.rebelgunworks.com.au" + str(n["href"]))
        p = Product(
            page = page,
            name = n.p.text,
            link = "https://www.rebelgunworks.com.au" + str(n["href"]),
            disclosure = dis
        )
        p.save()
    # scrap_completed(pk=page.pk)
    return scrap_completed(pk=page.pk)

class ScrapURLHandler(View):
    template_name = "scrapy_view.html"
    form_class = URLaddressForm
    def get(self, request):
        form = self.form_class(request.POST or None)
        links = URLaddress.objects.all()
        pages = Page.objects.filter(is_done=False)
        context = {
            "title": "scrapy",
            "form": form,
            "links": links,
            "pages": pages
        }
        return render(request, self.template_name, context)
    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect("scrapy:create_link")
            
def delete_link(request, pk):
    link = get_object_or_404(URLaddress, pk=pk)
    link.delete()
    return redirect("scrapy:create_link")

def view_pages(request, pk):
    link = get_object_or_404(URLaddress, pk=pk)
    context = {
        "title": "all pages",
        "link": link
    }
    return render(request, "page_list.html", context)

def get_all_urls(request, pk):
    link = get_object_or_404(URLaddress, pk=pk)
    url = link.url
    data = []
    pages = Page.objects.all()
    while True:
        soup = get_url(url)
        url = getnextpage(soup)
        data.append(url)
        print("sample product", url)
        if url:
            pages = Page(
                url_address = link,
                link = url
            )
            pages.save()
        if url == None:
            break
    return redirect("scrapy:pages", pk=link.pk)

class ProductsView(View):
    template_name = "product_list.html"
    initial = {'key': 'value'}
    def get(self, request):
        products = Product.objects.all()
        format_form = ProductFormat(initial=self.initial)
        context = {
            "title": "all products",
            "products": products,
            "format": format_form
        }
        return render(request, self.template_name, context)
    def post(self, request):
        qs = Product.objects.all()
        dataset = ProductResource().export(qs)
        format = request.POST.get('format')
        name = request.POST.get('name')
        if format == 'xls':
            ds = dataset.xls
        elif format == 'csv':
            ds = dataset.csv
        else:
            ds = dataset.json

        response = HttpResponse(ds, content_type = f'{format}')
        response["Content-Disposition"] = f"attachment; filename={name}.{format}"
        return response



# rest framework
class ProductViewset(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.exclude(disclosure=None)
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]