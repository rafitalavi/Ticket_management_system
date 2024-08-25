from django import forms

class TicketPurchaseForm(forms.Form):
    ticket_class = forms.CharField(widget=forms.HiddenInput())
    matchname = forms.CharField(widget=forms.HiddenInput())
    date = forms.CharField(widget=forms.HiddenInput())
    time = forms.CharField(widget=forms.HiddenInput())
    city = forms.CharField(widget=forms.HiddenInput())
    stad = forms.CharField(widget=forms.HiddenInput())
    price = forms.CharField(widget=forms.HiddenInput())
    transaction_id = forms.CharField(label='Transaction ID', required=True, widget=forms.TextInput(attrs={'class': 'text-dark'}))
