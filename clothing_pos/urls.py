"""
URL configuration for clothing_pos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from core.views import admin_dashboard
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', admin_dashboard, name='admin_dashboard'), # Dashboard
    path('sales/', include('sales.urls')),            # Sales/POS logic
    path('products/', include('products.urls')),      # Products logic
    path('reports/', include('reports.urls')),        # Reports logic
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)