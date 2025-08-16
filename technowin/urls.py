"""
URL configuration for technowin24 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Home.views import *
from django.urls import re_path
from django.views.static import serve
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap


sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin', admin.site.urls),
    path("", Home,name='Home'),
    path("Home", Home,name='Home'),
    path("index", Home,name='Home'),
    path('AboutUs', AboutUs, name='AboutUs'),
    path('aboutUs', AboutUs, name='AboutUs'),
    path('Services', Services, name='Services'),
    path('serviceLatest', Services, name='Services'),
    path('ContactUs', ContactUs, name='ContactUs'),
    path('contactUs', ContactUs, name='ContactUs'),
    path('Software', Software, name='Software'),
    path('softwareSolutions', Software, name='Software'),
    path('siteMap', siteMap, name='siteMap'),
    path('Product', Product, name='Product'),
    path('product', Product, name='Product'),
    path('Blogs', Blogs, name='Blogs'),
    path('AutomationExpo', AutomationExpo, name='AutomationExpo'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('get_botans', get_botans, name='get_botans'),
    path('website_counter/', website_counter, name='website_counter'),
    path('contactUsFormPost/', contactUsFormPost, name='contactUsFormPost'),
    path('aboutUsFormPost/', aboutUsFormPost, name='aboutUsFormPost'),
    re_path(r'^googleff696756859250e5\.html$', serve, {'document_root': settings.BASE_DIR, 'path': 'googleff696756859250e5.html'}),

]
