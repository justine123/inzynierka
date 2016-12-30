from django import forms


class ChooseAxisForm(forms.Form):
    temperature = forms.CheckboxInput()
    humidity = forms.CheckboxInput()
    wind_speed = forms.CheckboxInput()
    pm25 = forms.CheckboxInput()
    pm10 = forms.CheckboxInput()
    pressure = forms.CheckboxInput()


class ChooseCorrelationForm(forms.Form):
    temperature = forms.CheckboxInput()
    humidity = forms.CheckboxInput()
    wind_speed = forms.CheckboxInput()
    pm25 = forms.CheckboxInput()
    pm10 = forms.CheckboxInput()
    pressure = forms.CheckboxInput()
