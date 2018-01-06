from django.conf.urls import url
from paperreviewer.views import ReviewerProfileView


urlpatterns=[
    url(r'^profile/$', ReviewerProfileView.as_view(), name="profile"),
]