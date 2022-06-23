
from django import forms 
from django.forms import EmailInput, ModelForm
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill, Message 
from django.forms import Textarea, TextInput, EmailInput


class DeveloperForm(forms.Form): 
    name = forms.CharField(max_length=50)
    name.widget.attrs.update({
        'placeholder': 'Search our developers',
    })

    def __init__(self,*args,**kwargs): 
        super(DeveloperForm,self).__init__(*args,**kwargs)

        for key in self.fields:
            if key != 'tags':  
                self.fields[key].widget.attrs.update({'class': 'input'})
    

class CustomUserCreationForm(UserCreationForm):
    class Meta: 
        fields = ['first_name','email','username','password1','password2']
        model = User 
        labels = { 
            'first_name' : 'Name',
        }
    def __init__(self,*args,**kwargs): 
        super(CustomUserCreationForm,self).__init__(*args,**kwargs)

        for key in self.fields:
            if key != 'tags':  
                self.fields[key].widget.attrs.update({'class': 'input'})

class ProfileForm(ModelForm): 
    class Meta: 
        model = Profile 
        fields = '__all__'
        exclude = ['user']
    
    def __init__(self,*args,**kwargs): 
        super(ProfileForm,self).__init__(*args,**kwargs)

        for key in self.fields:
            if key != 'tags':  
                self.fields[key].widget.attrs.update({'class': 'input'})

class SkillForm(ModelForm): 
    class Meta: 
        model = Skill 
        fields = '__all__'
        exclude = ['owner']
        
        widgets= { 
            'name': TextInput(attrs={
                'size': 50,
                'class' : 'input',
                'placeholder':' Type your skill name',
                }),
        
            'description': Textarea(attrs= { 
                'class': 'input', 
                'placeholder': 'Describe your skill'
            })
        }
        
class MessageForm(ModelForm): 
    class Meta: 
        model = Message 
        fields = ['body']

        widgets = { 
            
            'body': Textarea(attrs= { 
                'class': 'input', 
                'placeholder': 'Type Yours text here'
            })

        }


