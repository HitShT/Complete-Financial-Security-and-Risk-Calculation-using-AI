from django.forms import ModelForm,modelformset_factory
from django import forms
from django.contrib.auth.models import User
from .models import presentAssetsData,presentLiabilitiesData,UserDependents,userIncomeData


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

dependentsFormset = modelformset_factory(
    UserDependents,
    fields=('dependents_age','dependents_name','dependents_relation'),
    extra=1,
    widgets={'dependents_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Name of Dependent'
        }),
            'dependents_age': forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Age of Dependent'
        }),
            'dependents_relation': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Relation with Dependent'
        }),
    }
)

class userIncomeDataForm(ModelForm):
    class Meta:
        model = userIncomeData
        fields = ["fixed_salary","variable_salary_min","variable_salary_max"]
