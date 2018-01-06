"""paper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from papermanager.views import CreatePaperView, EditPaperVersionsView,\
    AddPaperVersionView, ShowPaperVersionView, DownloadFile, SubmitPaperView

urlpatterns = [
    url(r'^createpaper/$', CreatePaperView.as_view(), name="createpaper"),
    url(r'^editpaperversions/(?P<slug>[\w-]+)/$',
        EditPaperVersionsView.as_view(), name="editpaperversions"),
    url(r'^editpaperversions/(?P<paperslug>[\w-]+)/(?P<versionslug>[\w-]+)/$',
         ShowPaperVersionView.as_view(), name="showpaperversion"),
    url(r'^submitpaperversion/(?P<paperslug>[\w-]+)/(?P<versionslug>[\w-]+)/$',
         SubmitPaperView.as_view(), name="submitpaper"),
    url(r'^downloadfile/(?P<paperslug>[\w-]+)/(?P<versionslug>[\w-]+)/(?P<filename>[.\w-]+)$',
         DownloadFile.as_view(), name="downloadfile"),
    url(r'^addpaperversions/(?P<paperslug>[\w-]+)/$',
         AddPaperVersionView.as_view(), name="addpaperversion"),
]
