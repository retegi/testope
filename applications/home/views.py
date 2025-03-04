from django.shortcuts import render
from django.views.generic import (
    TemplateView,
    ListView
)
from django.contrib.auth.models import User
from applications.learning.models import MyLearning, Topic, Ope
from django.http import HttpResponse

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm  # Importa el formulario






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



def formulario_contactar(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        company = request.POST.get("company", "")
        message = request.POST.get("message", "")
        recaptcha_response = request.POST.get("g-recaptcha-response")

        # Validar reCAPTCHA con Google
        recaptcha_verify = requests.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={
                "secret": settings.RECAPTCHA_PRIVATE_KEY,
                "response": recaptcha_response,
            }
        ).json()

        if not recaptcha_verify.get("success"):
            messages.error(request, "Error: reCAPTCHA inválido. Intenta nuevamente.")
            return render(request, "home/index.html", {
                "name": name,
                "email": email,
                "phone": phone,
                "company": company,
                "message": message
            })

        # Enviar correo con los datos ingresados desde la web
        asunto = f"Tu Asistente Inteligente Nuevo mensaje de contacto de {name}"
        contenido = (
            f"Nombre: {name}\n"
            f"Email: {email}\n"
            f"Teléfono: {phone}\n"
            f"Empresa: {company}\n"
            f"Mensaje:\n{message}"
        )

        try:
            send_mail(
                asunto,
                contenido,
                settings.EMAIL_HOST_USER,  # Remitente
                ["euskodev@gmail.com"],  # Cambia por el correo real
                fail_silently=False,
            )
            messages.success(request, "Tu mensaje ha sido enviado con éxito.")
            return redirect("home_app:home")

        except Exception as e:
            messages.error(request, f"Error al enviar el correo: {str(e)}")
            return render(request, "home/index.html", {
                "name": name,
                "email": email,
                "phone": phone,
                "company": company,
                "message": message
            })

    return redirect("home_app:home")

