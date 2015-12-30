from django.conf.urls import patterns, url
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^login$', 'accounts.views.persona_login', name="persona_login"),
    url(r'^logout$', logout, {"next_page": "/"}, name="persona_logout")
]
