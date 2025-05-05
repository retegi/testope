from os import name
from django.urls import include, path
from . import views


app_name = 'home_app'

urlpatterns = [
    path('',
        views.HomePageView.as_view(),
        name='home',
    ),
    path('aviso_legal/',
        views.AvisoLegalView.as_view(),
        name='aviso_legal',
    ),
    path('politica_de_privacidad/',
        views.PoliticaDePrivacidadView.as_view(),
        name='politica_de_privacidad',
    ),
    path('politica_de_cookies/',
        views.PoliticaDeCookiesView.as_view(),
        name='politica_de_cookies',
    ),
    path('contact/',
        views.ContactView.as_view(),
        name='contactar',
    ),


    path('preguntas/',
        views.PreguntasView.as_view(),
        name='pregunta',
    ),


    path('donativos/',
        views.DonativosView.as_view(),
        name='donativos',
    ),

    path('sobre-nosotros/',
        views.SobrenosotrosView.as_view(),
        name='sobre-nosotros',
    )

]