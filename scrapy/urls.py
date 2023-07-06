from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewset)

app_name = "scrapy"
urlpatterns = [
    # path('', views.get_all_urls, name='home'),
    path('', views.ScrapURLHandler.as_view(), name='create_link'),
    path('delete/<pk>', views.delete_link, name='delete'),
    path('pages/<pk>', views.view_pages, name='pages'),
    path('get-pages/<pk>', views.get_all_urls, name='get_pages'),
    path('products/', views.ProductsView.as_view(), name='product'),
    path('products/is-done/<pk>', views.scrap_completed, name='completed'),
    path('products/pages/<pk>', views.get_products, name='product_pages'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]