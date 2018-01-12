from django.conf.urls import url
from paperreviewer.views import ReviewerProfileView, ReviewPaperView,\
    ReviewPaperVersionView, ReviewPaperAcceptedView, ReviewPaperRejectedView,\
    ReviewDownloadFileView, ExposedPDFRecieve, EditPDFView, ExposedPDFDownload


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
    url(r'^reviewpaperedit/(?P<paperslug>[\w-]+)/(?P<versionslug>[\w-]+)/(?P<fileslug>[\w-]+)$', EditPDFView.as_view(),
         name="reviewpaperedit"),
    url(r'exposedpdfrecieve/(?P<fileslug>[\w-]+)$', ExposedPDFRecieve.as_view(),
         name="exposedpdfrecieve"),
    url(r'exposedpdfdownload/(?P<fileslug>[\w-]+)$', ExposedPDFDownload.as_view(),
         name="exposedpdfdownload"),
]