from django.db import models
from django.contrib.auth.models import User
import uuid 
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
# Create your models here.


class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=False)
    username = models.CharField(max_length=100,null=True, blank=True)
    location = models.CharField(max_length=100,null=True, blank=False)
    email = models.EmailField(max_length=500,null=True, blank=True)
    short_intro = models.CharField(max_length=500,null=True,blank=True)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(null=True,
                    blank=True, upload_to='profiles/', default='profiles/default-profile.JPG')
    social_github = models.CharField(max_length=100,null=True, blank=True )
    social_twiter = models.CharField(max_length=100,null=True, blank=True )
    social_linkedin = models.CharField(max_length=100,null=True, blank=True )
    social_youtube = models.CharField(max_length=100,null=True, blank=True )
    social_website = models.CharField(max_length=100,null=True, blank=True )
    created = models.DateField(auto_now_add=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=False)
    def __str__(self): 
        return str(self.name)

    @property 
    def imageURL(self): 
        try: 
           url = self.profile_image.url[:28]+'.eu-south-1.' + self.profile_image.url[29:]
           
        except: 
            url = ''
        return url 
    class Meta: 
        ordering = ['created']


class Skill(models.Model): 
    owner = models.ForeignKey(Profile, 
            on_delete=models.CASCADE, null=True,blank=True) 
    name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True,blank=True)
    created = models.DateField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=False)
    
    def __str__(self): 
        return str(self.name)

class Message(models.Model): 
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)
    recepient = models.ForeignKey(Profile,on_delete=models.SET_NULL, null=True, related_name='messages')
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200,blank=True, null=True)
    subject = models.CharField(max_length=200,blank=True, null=True)
    body = models.TextField()
    chat_room = models.ForeignKey('Chat', on_delete=models.CASCADE, null=True,related_name='messages')
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(default=timezone.now)
    id = models.UUIDField(default=uuid.uuid4, unique=True, 
                            primary_key=True, editable=False)

    def __str__(self): 
        if self.subject: 
            return self.subject
        else: 
            return 'No subject'
    
    class Meta: 
        ordering = ['is_read','created']

class Chat(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True, 
                primary_key=True, editable=False)
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True)
    recepient = models.ForeignKey(Profile,on_delete=models.SET_NULL, null=True, related_name='chats')
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(default=timezone.now)
            
    def __str__(self): 
        return str(self.unique_id)
    
    class Meta: 
        ordering = ['-modified']