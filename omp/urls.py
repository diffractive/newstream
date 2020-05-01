from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls

from donations.views import CustomPasswordResetView
from django.contrib.auth import views
from django.urls import path
import omp.views as user_views

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/autocomplete/', include(autocomplete_admin_urls)),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('search/', search_views.search, name='search'),

    path('donations/', include('donations.urls')),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),


    # password_reset* are meant for forgot password path
    path('password_reset/',
         CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('verify-email/<uidb64>/<token>/', user_views.verify_email,
         name='verify-email'),
    path('personal-info/', user_views.personal_info, name='personal-info'),
    path('resend-verification-email/', user_views.resend_verification_email,
         name='resend-verification-email'),
    path('personal-info/change-email-address/', user_views.change_email_address,
         name='change-email-address'),
    path('security/', user_views.security, name='security'),
    path('security/change-password/', user_views.change_password,
         name='change-password'),
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
