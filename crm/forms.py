from django import forms
from .models import Record
from .models import Project
from captcha.fields import CaptchaField

# record form
class AddRecordForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(
            attrs={"placeholder":"First Name", "class":"form-control"}),
        label="")
    last_name = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(
            attrs={"placeholder":"Last Name", "class":"form-control"}),
        label="")
    email = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(
            attrs={"placeholder":"Email", "class":"form-control"}),
        label="")
    phone = forms.CharField(
        required=True, 
        widget=forms.widgets.TextInput(
            attrs={"placeholder":"Phone", "class":"form-control"}),
        label="")
    
    class Meta:
        model = Record
        exclude = ("user",)

# contact form
from django.utils.safestring import mark_safe

class ContactForm(forms.Form):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "First Name", "class": "form-control"}),
        label="First Name"
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Last Name", "class": "form-control"}),
        label="Last Name"
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Email", "class": "form-control"}),
        label="Email Address"
    )
    phone = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Phone", "class": "form-control"}),
        label="Phone Number"
    )
    address = forms.CharField(
        max_length=255,
        required=False,  # Optional field
        widget=forms.TextInput(attrs={"placeholder": "Project Address", "class": "form-control"}),
        label="Project Address"
    )
    subject = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Subject", "class": "form-control"}),
        label="Project Subject"
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Tell us about your project...", "rows": 5, "class": "form-control"}),
        label="Message"
    )
    captcha = CaptchaField(
        label="Type what you see"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.label = mark_safe(f"{field.label} <span class='text-danger'>*</span>")

# project form
class AddProjectForm(forms.ModelForm):
    address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Street Address", "class": "form-control"}),
        label=""
    )
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "City", "class": "form-control"}),
        label=""
    )
    state = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "State", "class": "form-control"}),
        label=""
    )
    zipcode = forms.CharField(
        max_length=25,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Zipcode", "class": "form-control"}),
        label=""
    )
    description = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.Textarea(attrs={"placeholder": "Project Description", "rows": 5, "class": "form-control"}),
        label=""
    )


    class Meta:
        model = Project
        exclude = ('user', 'client_record')
        widgets = {
            'estimate_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }