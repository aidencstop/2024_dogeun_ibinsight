"""
URL configuration for ibinsight project.

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
from django.urls import include, path
from django.conf import settings #요거
from django.conf.urls.static import static #이 두줄과
from member.views import member_login
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.to_index, name='to-index'),
    path('sign_up/', views.to_sign_up, name='to-sign_up'),
    path('main/', views.to_main, name='to-main'),
    path('login/', views.login, name='login'),
    path('survey/', views.to_survey, name='to-survey'),
    path('recommend/', views.recommend, name='recommend'),
    path('logout/', views.log_out, name='log-out'),
    path('about_ib/', views.to_about_ib, name='to-about_ib'),
    path('about_ib_course_search/', views.to_about_ib_course_search_default, name='to-about_ib_course_search-default'),
    path('about_ib_course_search/<int:pk>/', views.to_about_ib_course_search, name='to-about_ib_course_search'),
    path('forum/', include('forum.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #이 줄 추가

