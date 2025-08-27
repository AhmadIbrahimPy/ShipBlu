"""
URL configuration for core_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include  # Import path for URL routing and include to include other URL configs
from backend.orders import urls as orders_urls  # Import the URLs from the 'orders' app and alias them

# Define the main URL patterns for the project
urlpatterns = [
    path('app/', include(orders_urls)),  # Include all URLs from 'orders' app under the 'app/' prefix
]