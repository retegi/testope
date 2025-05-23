from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here



class Ope(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    entity = models.CharField(max_length=50, blank=True, null=True)
    dateTime = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    locality = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    autonomousCommunity = models.CharField(max_length=50, blank=True, null=True)
    shortDescription = models.TextField(max_length=500, verbose_name="Descripción breve", null=True, blank=True)
    longDescription = models.TextField(max_length=10000, verbose_name="Descripción completa", null=True, blank=True)
    urlOpe = models.URLField(max_length=1000, verbose_name="Enlace de la Ope", null=True, blank=True)
    published = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.name



class Topic(models.Model):
    number = models.IntegerField(blank=True, null=True)
    ope = models.ForeignKey(Ope, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    def __str__(self):
        return self.name

correctAnswer = [('A','A'),('B','B'),('C','C'),('D','D'),('No detallado','No detallado')]

class Test(models.Model):
    ope = models.ForeignKey(Ope, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey(Topic, max_length=200, blank=True, null=True, on_delete=models.CASCADE)
    number = models.IntegerField(blank=True, null=True)
    question = models.TextField(max_length=500, blank=True, null=True)
    aAnswer = models.CharField(max_length=350, blank=True, null=True)
    bAnswer = models.CharField(max_length=350, blank=True, null=True)
    cAnswer = models.CharField(max_length=350, blank=True, null=True)
    dAnswer = models.CharField(max_length=350, blank=True, null=True)
    correctAnswer = models.CharField(choices=correctAnswer,max_length=15, blank=True, null=True)
    def __str__(self):
        return self.question


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(blank=True, null=True)
    ope = models.ForeignKey(Ope,max_length=30,blank=True, null=True, on_delete=models.CASCADE)
    answerProgresionCorrect = models.IntegerField(blank=True, null=True)
    correctAnswerCounterTotal = models.IntegerField(blank=True, null=True) #Si se redsponde incorrecto se resetea a cero
    incorrectAnswerCounterTotal = models.IntegerField(blank=True, null=True)
    questionCircleCounter = models.IntegerField(blank=True, null=True)
    lastAnsweredQuestion = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(default=timezone.now, null=True)
    def __str__(self):
        return str(self.id)
    
class MyLearning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ope = models.ForeignKey(Ope, on_delete=models.CASCADE, null=True, blank=True)
    datetime = models.DateTimeField(default=timezone.now, null=True)
    def __str__(self):
        return str(self.ope)
    