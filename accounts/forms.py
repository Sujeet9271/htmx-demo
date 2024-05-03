from datetime import datetime, date
from django import forms

from accounts.models import Event, Tickets



class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'min': date.today(), 'value':date.today()}))

    class Meta:
        model = Event
        fields = '__all__'


class TicketsForm(forms.ModelForm):

    class Meta:
        model = Tickets
        fields = '__all__'