from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from landing_page.sitemap import LearnSitemap

urlpatterns = [
    path('', include('mainpage.urls')),

    path('admin/', admin.site.urls),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": {"static": LearnSitemap}},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
