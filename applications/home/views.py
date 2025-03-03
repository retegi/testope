from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView
)
from django.contrib.auth.models import User
from applications.learning.models import MyLearning, Topic, Ope
from django.http import HttpResponse


class HomePageView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user']=self.request.user
        context['myLearning']=MyLearning.objects.filter(user=self.request.user.id)
        #context['category']=Category.objects.all()
        context['countUsersRegistered']=13603
        context['countUsersLearning']=539
        context['ope']=Ope.objects.all()
        context['locality']=Ope.objects.all().distinct()
        return context
    
    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        answer_dePosta = request.POST.get('','')  # Obtener el valor del campo 'opciones'
        # Aquí puedes procesar la opción seleccionada como lo necesites
        categoryId = request.POST.get('categoryId', '')
        user = self.request.user
        myLearning = MyLearning()
        myLearning.user = self.request.user
        myLearning.category = Category.objects.get(id=categoryId)
        try:
            ifThisCategoryExistInUser = MyLearning.objects.get(category=categoryId, user=user)
        except:
            myLearning.save()
        context['myLearning']=MyLearning.objects.filter(user=self.request.user)
        context['category']=Category.objects.all()
        return render(request, 'home/index.html', context)

class AvisoLegalView(TemplateView):
    template_name = "home/aviso_legal.html"

class PoliticaDePrivacidadView(TemplateView):
    template_name = "home/politica_de_privacidad.html"

class PoliticaDeCookiesView(TemplateView):
    template_name = "home/politica_de_cookies.html"

class ContactView(TemplateView):
    template_name = "home/contactar.html"

class PreguntasView(TemplateView):
    template_name = "home/preguntas.html"

class DonativosView(TemplateView):
    template_name = "home/donativos.html"

class SobrenosotrosView(TemplateView):
    template_name = "home/sobrenosotros.html"


