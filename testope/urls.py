
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import HttpResponseRedirect

"""urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include('allauth.urls')),
    path('assistant/', include('applications.assistant.urls')),
    path('', include('applications.home.urls')), 
]"""

urlpatterns = [
    path('', lambda request: HttpResponseRedirect(f'/{settings.LANGUAGE_CODE.split("-")[0]}/')),
    path('admin/', admin.site.urls),
    path('assistant/', include('applications.assistant.urls')),
]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls')),
    ]

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
     # Reemplaza 'yourapp' por tu aplicación real
    path('', include('applications.learning.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('applications.home.urls')),
)