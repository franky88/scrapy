from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from bs4 import BeautifulSoup
import requests
# Create your views here.
def home(request):
    return HttpResponse("Hello it is working!")

class ScrapyView(View):
    template_name = "scrapy_view.html"
    context = {
        "title": "scrapy views",
    }
    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            url_queries = request.GET.get('q')
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Accept-Language": "en",
            }
            productURL = requests.get(url_queries, headers=headers)
            doc = BeautifulSoup(productURL.text, "html.parser")
            all_links = doc.find_all("a", class_="product-grid-item")
            # print(all_links)
            for link in all_links:
                link = link.string
                print(link)
            context = {
                "title": "scrapy",
                "alllinks": link,
            }
            return render(request, self.template_name, context)