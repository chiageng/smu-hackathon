from django import forms 
from django.contrib.auth.models import User
from app.models import UserProfileInfo, TemplateFile, File

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User 
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_pic',) # 'portfolio_site' )

class TemplateUpload(forms.ModelForm):
    class Meta:
        model = TemplateFile
        fields = ["name", "filepath"]

class FileUpload(forms.ModelForm):         #For regular files/reviewing
    class Meta:
        model = File
        fields = ["name", "filepath"]

class GenerateForm(forms.Form):
    def __init__(self, templates, files, *args, **kwargs):
        super().__init__(*args, **kwargs)
        t_choices = [(template.filepath, template.name) for template in templates]
        self.fields['template'] = forms.ChoiceField(choices = t_choices, label='Template')

        f_choices = [(file.filepath, file.name) for file in files]
        self.fields['file'] = forms.ChoiceField(choices = f_choices, label='Data file')