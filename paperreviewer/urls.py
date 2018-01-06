from django.conf.urls import url
from paperreviewer.views import ReviewerProfileView, ReviewPaperView


urlpatterns=[
    url(r'^profile/$', ReviewerProfileView.as_view(),
         name="profile"),
    url(r'^reviewPaper/(?P<paperslug>[\w-]+)/$', ReviewPaperView.as_view(),
         name="reviewpaper"),
]