"""
Default urls for django Organice
"""
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^newsletter/', include('emencia.django.newsletter.urls.newsletter')),
    url(r'^newsletter/', include('emencia.django.newsletter.urls.mailing_list')),
    url(r'^newsletter/track/', include('emencia.django.newsletter.urls.tracking')),
    url(r'^newsletter/stats/', include('emencia.django.newsletter.urls.statistics')),
    url(r'^artikel/', include('zinnia.urls')),
    url(r'^', include('cms.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)