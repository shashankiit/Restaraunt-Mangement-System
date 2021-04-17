from django.forms import ModelForm
from .models import menu_items

class OrderForm(forms.Form):
    menuits = forms.MultipleChoiceField(c)
    class Meta:
        model = menu_items
        fields = '__all__'