"""elizabetstienstra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.static import serve

from .sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("", include("home.urls")),
    path("about/", include("about.urls")),
    path("cv/", include("cv.urls")),
    path("info/", include("info.urls")),
    path("oeuvre/", include("oeuvre.urls")),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('sitemap.xml', sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
