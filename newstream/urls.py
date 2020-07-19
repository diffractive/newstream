from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls

from django.urls import path
import newstream.views as user_views

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/autocomplete/', include(autocomplete_admin_urls)),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),

    path('donations/', include('donations.urls')),

    path('accounts/', include('allauth.urls')),

    path('personal-info/', user_views.personal_info, name='personal-info'),
    path('security/', user_views.security, name='security'),
    path('advanced-settings/', user_views.advanced_settings,
         name='advanced-settings'),
    path('advanced-settings/delete-account/', user_views.delete_account,
         name='delete-account'),
    path('unsubscribe/<email>/<hash>/', user_views.unsubscribe,
         name='unsubscribe'),

]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r"", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r"^pages/", include(wagtail_urls)),
]
