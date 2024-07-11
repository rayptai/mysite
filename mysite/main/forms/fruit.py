from django import forms


class FruitForm(forms.Form):
    mass = forms.FloatField(label='mass')
    width = forms.FloatField(label='width')
    height = forms.FloatField(label='height')
