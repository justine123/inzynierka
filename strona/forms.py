from django import forms

DISPLAY_CHOICES = (
    ("temperature", "Display Temperature"),
    ("humidity", "Display Humidity"),
    ("pollution", "Display Pollution")
)


class EntryForm(forms.Form):
    display_type = forms.ChoiceField(widget=forms.RadioSelect, choices=DISPLAY_CHOICES)
