from django.forms import ModelForm,modelformset_factory
from django import forms
from django.contrib.auth.models import User
from Base.models import presentAssetsData,presentLiabilitiesData

class Register(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required = True)
    class Meta:
        model = User
        fields = ["username","email","password"]

class userLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

assetFormset = modelformset_factory(
    presentAssetsData,
    fields=('assets_name','assets_valuation'),
    extra=1,
    widgets={'assets_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Name'
        }),
        'assets_valuation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Value'
            }),
    }
)

liabilitesFormset = modelformset_factory(
    presentLiabilitiesData,
    fields=('liabilities_name','liabilities_valuation'),
    extra=1,
    widgets={'liabilities_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Name'
        }),
        'liabilities_valuation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Value'
            })
    }
)
