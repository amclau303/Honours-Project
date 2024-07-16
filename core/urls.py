"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('bar_chart', views.bar_chart, name='bar_chart'),
    path('line_chart', views.line_chart, name='line_chart'),
    path('scatter_plot', views.scatter_plot, name='scatter_plot'),
    path('stacked_bar_chart', views.stacked_bar_chart, name='stacked_bar_chart'),
    path('thyroid_map', views.thyroid_map_view, name='thyroid_map'),
    path('patient_data', views.plot_visualizations, name='patient_data'),
    path('hyper_hypo', views.hyper_hypo, name='hyper_hypo'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('plotly_view', views.plotly_view, name='plotly_view')
]
