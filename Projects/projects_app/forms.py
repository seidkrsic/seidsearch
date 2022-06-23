
from django.forms import ModelForm 
from .models import Project, Review
from django import forms 

class ProjectForm(ModelForm):
    class Meta: 
        model = Project 
        fields = ['title', 'description', 'demo_link','source_link','featured_image'] 
        # widgets = {
        #     'tags' : forms.CheckboxSelectMultiple(),
        # }
    
    def __init__(self,*args,**kwargs): 
        super(ProjectForm,self).__init__(*args,**kwargs)

        for key in self.fields:
            if key !='tags':  
                self.fields[key].widget.attrs.update({'class': 'input'})
        self.fields['title'].widget.attrs.update({'placeholder': 'Search projects'})


class ReviewForm(ModelForm): 
    class Meta: 
        model = Review 
        fields = ['value', 'body']
    
    labels = { 
        'value' : 'Place your vote here: ',
        'body' : 'Add a comment with your vote here',
    }

    def __init__(self,*args,**kwargs): 
        super(ReviewForm,self).__init__(*args,**kwargs)

        for key in self.fields:
            if key != 'tags':  
                self.fields[key].widget.attrs.update({'class': 'input'})
