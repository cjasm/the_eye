"""theeye URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework import routers, permissions
from theeye.core.views import EventViewSet, ErrorViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="The Eye API",
      default_version='v1',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="cjasm@cin.ufpe.br"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.SimpleRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'errors', ErrorViewSet, basename='error')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
]
