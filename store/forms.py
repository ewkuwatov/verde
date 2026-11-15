from django import forms

from .models import Subscriber


class CheckoutForm(forms.Form):
    name = forms.CharField(label="Как к вам обращаться", max_length=120)
    phone = forms.CharField(label="Номер телефона", max_length=40)
    email = forms.EmailField(label="Электронная почта", required=False)
    address = forms.CharField(label="Адрес доставки", max_length=240)
    comment = forms.CharField(label="Комментарий к заказу", required=False, widget=forms.Textarea(attrs={"rows": 3}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-input"


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ["email"]
        widgets = {"email": forms.EmailInput(attrs={"placeholder": "Ваш email", "class": "newsletter-input"})}
