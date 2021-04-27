from django.forms import ModelForm,modelformset_factory
from django import forms
from django.contrib.auth.models import User
from .models import presentAssetsData,presentLiabilitiesData,UserDependents,userIncomeData,addUserExpense,addUserInvestment,allPredictionsData

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

class allPredictionsDataForm(ModelForm):

    def __init__(self, *args, **kwargs):
       super(allPredictionsDataForm, self).__init__(*args, **kwargs)
       # self.fields['monthly_salary'].widget.attrs['readonly'] = True
       # self.fields['investmentTotal'].widget.attrs['readonly'] = True
       # self.fields['investmentMonthly'].widget.attrs['readonly'] = True
       # self.fields['yearly_expense'].widget.attrs['readonly'] = True
       # self.fields['monthly_expense'].widget.attrs['readonly'] = True
       # self.fields['dependents'].widget.attrs['readonly'] = True

    class Meta:
        model = allPredictionsData
        fields = [
            "age",
            "healthInsurance"
            ]

    # results = [
    #     monthly_salary1,
    #     previousInvestment,
    #     monthlyInvestment,
    #     expense_yearly,
    #     expense_monthly,
    #     dependentsCount
    #     ]

userExpenseFormset = modelformset_factory(
    addUserExpense,
    fields = ("expense_name","expense_date","expense_amount","expense_repeat_frequency"),
    extra = 1,
    widgets = {
        "expense_name": forms.TextInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Enter Name of Expense'
        }),
        "expense_date": forms.DateInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Enter Date of Expense',
            'type' : 'date'
        }),
        "expense_amount": forms.NumberInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Enter amount of Expense'
        }),
        "expense_repeat_frequency": forms.NumberInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Enter how often in months expense repeats'
        }),
    }
)

userInvestmentFormset = modelformset_factory(
    addUserInvestment,
    fields = ("investment_name","investment_date","investment_amount","investment_repeat_frequency"),
    extra = 1,
    widgets = {
        "investment_name": forms.TextInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Enter Name of Investment'
        }),
        "investment_date": forms.DateInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Enter Date of Investment',
            'type' : 'date'
        }),
        "investment_amount": forms.NumberInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Enter amount of Investment'
        }),
        "investment_repeat_frequency": forms.NumberInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Enter how often in months investment repeats'
        }),
    }
)
