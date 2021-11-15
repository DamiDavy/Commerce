from django import forms

class AuctionForm(forms.Form):
	title = forms.CharField(label='Title', max_length=64, 
	widget=forms.TextInput(attrs={'class': "form-control"}))
	description = forms.CharField(label="Description", 
	widget=forms.Textarea(attrs={'class': "form-control", 'rows': "3"}))
	startbid = forms.DecimalField(label="Start Bid", max_digits=8, 
	decimal_places=2, widget=forms.NumberInput(attrs={'class': "form-control"}))
	file = forms.FileField(label="Image File", 
	widget=forms.ClearableFileInput(attrs={'class': "form-control"}))
