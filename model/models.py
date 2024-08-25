from contextlib import nullcontext
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class City(models.Model):
    name=models.CharField(max_length=255)
    city_manager = models.Manager()
    class Meta:
        ordering=['name']
        verbose_name_plural='City'
    def __str__(self) -> str:
        return self.name
class Stadium(models.Model):
    nameofstadium=models.CharField(max_length=255)
    class Meta:
        ordering=['nameofstadium']
        verbose_name_plural='Stadium'
    def __str__(self) -> str:
        return self.nameofstadium
class matchlist(models.Model):
    match=models.CharField(max_length=255)
    class Meta:
        ordering=['match']
        verbose_name_plural='matchlist'
    def __str__(self) -> str:
        return self.match
class TICKET(models.Model):
    city=models.ForeignKey(City,related_name='city',on_delete=models.CASCADE)
    stad=models.ForeignKey(Stadium,related_name='stad',on_delete=models.CASCADE)
    matchname=models.ForeignKey(matchlist,related_name='matches',on_delete=models.CASCADE)
    price=models.IntegerField()
    is_sold=models.BooleanField(default='False')
    Ticketclass=models.CharField(max_length=255)
    Date=models.DateField()
    Time=models.TimeField()
    def __iter__(self):
        return self.matchname
class USER(models.Model):
    nid=models.IntegerField(blank=True)
    passport=models.CharField(max_length=255,blank=True)
# class purchased_ticket(models.Model):
#     ticket_class=models.CharField(max_length=255)
#     matchname=models.CharField(max_length=255)
#     Date=models.DateField()
#     Time=models.TimeField()
#     city=models.CharField(max_length=255)
#     stad=models.CharField(max_length=255)
#     price=models.IntegerField()
#     transaction_id=models.CharField(max_length=255)