from django.conf.urls import url
from paperreviewer.views import ReviewerProfileView, ReviewPaperView,\
    ReviewPaperVersionView, ReviewPaperAcceptedView, ReviewPaperRejectedView,\
    ReviewDownloadFileView


urlpatterns=[
    url(r'^profile/$', ReviewerProfileView.as_view(),
         name="profile"),
    url(r'^reviewPaper/(?P<paperslug>[\w-]+)/$', ReviewPaperView.as_view(),
         name="reviewpaper"),
    url(r'^reviewPaper/(?P<paperslug>[\w-]+)/(?P<versionslug>[\w-]+)/$', ReviewPaperVersionView.as_view(),
         name="reviewpaperversion"),
    url(r'^reviewPaper/(?P<paperslug>[\w-]+)/(?P<versionslug>[\w-]+)/accept$', ReviewPaperAcceptedView.as_view(),
         name="reviewpaperaccept"),
    url(r'^reviewPaper/(?P<paperslug>[\w-]+)/(?P<versionslug>[\w-]+)/reject$', ReviewPaperRejectedView.as_view(),
         name="reviewpaperreject"),
    url(r'^download/(?P<paperslug>[\w-]+)/(?P<versionslug>[\w-]+)/(?P<fileslug>[\w-]+)$', ReviewDownloadFileView.as_view(),
         name="reviewpaperdownload"),
]