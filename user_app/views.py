from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect 

from user_app.utils import InboxPagination, searchInbox, searchProfiles 
from user_app.forms import DeveloperForm
from .models import Chat, Profile, Skill
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from user_app.utils import pagePagination 
from .forms import CustomUserCreationForm, SkillForm, MessageForm
from django.db.models import Q 
from .forms import ProfileForm

from user_app.models import Message

from django.utils import timezone 

# Create your views here





def loginPage(request):
    page = 'login'
    if request.user.is_authenticated: 
        return HttpResponseRedirect(reverse('index_user'))

    if request.method =="POST": 
        username = request.POST['username']
        password = request.POST['password']

        try: 
            user = User.objects.get(username=username)
        except: 
            messages.error(request,'User does not exists.')
            return render(request,'user_app/login.html', {})

        user = authenticate(request,username=username,password=password)
        
        if user is not None: 
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'index_user')
        else: 
            messages.error(request,'Username or password is incorrect.')
            return render(request,'user_app/login.html', {})        
    return render(request,'user_app/login.html', {
        'page':page,
    })

def logoutPage(request): 
    messages.info(request,f"{request.user} logged out.")
    logout(request)
    return HttpResponseRedirect(reverse('index_user'))

def registerUser(request): 
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST": 
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,f"{user} created.")
            login(request,user)
            return HttpResponseRedirect(reverse('index_user'))
        else: 
            messages.error(request,'Passwords do not match or username is taken.')
    return render(request,'user_app/login.html', {
        'page' : page,
        'form' : form,
    })

def index_user(request):
    page = request.GET.get('page')
    if request.method == 'GET': 
        if request.GET.get('name'):
            profiles , form = searchProfiles(request)
            profiles, paginator, custom_range = pagePagination(request,profiles,page)
            form = DeveloperForm(request.GET)
        else: 
            profiles = Profile.objects.all()
            profiles, paginator, custom_range = pagePagination(request,profiles,page)
            form = DeveloperForm()

    return render(request,'user_app/index.html', {
        'profiles': profiles,  
        'form' : form,
        'paginator': paginator, 
        'custom_range': custom_range,
        })
    

def profile(request, pk): 
    user1 = Profile.objects.get(id=pk)
    topSkills = user1.skill_set.exclude(description__exact="")
    otherSkills = user1.skill_set.filter(description="")
    return render(request,'user_app/profile.html', { 
        'user1' : user1, 
        'topSkills': topSkills,
        'otherSkills': otherSkills,
    })

@login_required(login_url='login')
def userAccount(request):
    print(request.user.profile.imageURL)
    user1 = request.user.profile
    skills = user1.skill_set.all()
    context = { 'user1' : user1, 
                'skills': skills,
    }
    return render(request,'user_app/account.html',context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile 
    form = ProfileForm(instance=profile)
    if request.method == 'POST': 
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        print(request.POST)
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect(reverse('account')) 
        else: 
            messages.error(request,'Not valid data sent.')      
    context = {'form':form}
    return render(request,'user_app/profile-form.html', context)


@login_required(login_url='login')
def createSkill(request): 
    page = 'create'
    profile = request.user.profile 
    if request.method == 'POST': 
        form = SkillForm(request.POST)
        if form.is_valid(): 
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,'Skill was added.') 
            return HttpResponseRedirect(reverse('account'))
    else: 
        form = SkillForm()
    context = {'form':form, 'page':page}
    return render(request,'user_app/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request,pk): 
    page = 'update'
    profile = request.user.profile 
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    if request.method == 'POST': 
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid(): 
            form.save()
            messages.success(request,'Skill was updated.') 
            return HttpResponseRedirect(reverse('account'))
    else: 
        context = {'form':form, 'page': page}
        return render(request,'user_app/skill_form.html', context)

@login_required(login_url='login')    
def deleteSkill(request,pk):
    page = 'skill'
    profile = request.user.profile 
    skill = profile.skill_set.get(id=pk) 
    if request.method == 'POST': 
        skill.delete()
        messages.success(request,'Skill was deleted.')
        return HttpResponseRedirect(reverse('account'))
    else: 
        context = {'project': skill, 'page': page, 'profile':profile}
        return render(request,'projects_app/delete.html',context) 




@login_required(login_url='login')
def inbox(request): 
    page = request.GET.get('page')
    chat_rooms = searchInbox(request)
    chat_rooms, paginator, custom_index = InboxPagination(request, chat_rooms, page)
    

    return render(request,'user_app/inbox.html', { 
        'chat_rooms' : chat_rooms,
        'paginator' : paginator, 
        'custom_index' : custom_index,
        'page' : page,
    })

@login_required(login_url="login")
def messageView(request,pk): 
    chat = Chat.objects.get(unique_id=pk)
    form = MessageForm()
    if chat.sender.id == request.user.profile.id:
        sender_id = chat.recepient.id
    else: 
        sender_id = chat.sender.id

    return render(request,'user_app/message.html', { 
        'chat' : chat.messages.all().order_by('-created')[:5],
        'form' : form, 
        'sender_id' : sender_id,
    })

@login_required(login_url='login')
def createMessage(request,pk): 
    recepient = Profile.objects.get(id=pk)
    form = MessageForm()
    
    if request.method == "POST": 
        sender = request.user.profile
        try:
            chat_room = Chat.objects.get(sender=sender, recepient=recepient)
        except:
            try: 
                chat_room = Chat.objects.get(sender=recepient, recepient=sender)
            except:
                chat_room = Chat.objects.create(sender=sender, recepient=recepient)
        
        
        form = MessageForm(request.POST) 
        if form.is_valid(): 
            message = form.save(commit=False)
            message.sender = sender 
            message.recepient = recepient 
        
        if sender: 
                message.name = sender.name 
                message.email = sender.email 
                message.chat_room = chat_room
        chat_room.modified = timezone.now()
        chat_room.save()
        message.save()

        return redirect('message',pk=chat_room.unique_id)

    return render(request,'user_app/message_form.html', { 
        'form' : form,
        'recepient' : recepient,
    })