from django.db import models

# Create your models here.



class Event(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    date = models.DateField()


    def __str__(self) -> str:
        return f'{self.name}-{self.address}'
    

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['-id']



class Users(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering=['id']


class Project(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Project'
        verbose_name_plural='Projects'

class Menu(models.Model):
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='menu')
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Menu'
        verbose_name_plural='Menus'

class SubMenu(models.Model):
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='submenu')
    menu_id = models.ForeignKey(Menu,on_delete=models.CASCADE,related_name='submenu')
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name='Sub Menu'
        verbose_name_plural='Sub Menus'


class Tickets(models.Model):
    number = models.CharField(max_length=100)
    project_id = models.ForeignKey(Project,on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    menu_id = models.ForeignKey(Menu,on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    submenu_id = models.ForeignKey(SubMenu,on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')

    def __str__(self):
        return self.number
    
    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
