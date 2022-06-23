

from django.db.models import Q 
from django.http import HttpResponseRedirect
from django.shortcuts import render
from zmq import Message
from user_app.forms import DeveloperForm
from projects_app.forms import ProjectForm, ReviewForm
from .models import Project
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user_app.models import Profile 
from projects_app.models import Tag 
from projects_app.utils import searchProjects, pagePagination
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

def index(request): 
    page = request.GET.get('page')
    if request.GET.get('title'): 
        projects, form = searchProjects(request)
        projects, paginator, custom_range = pagePagination(request,projects,page)
        form = ProjectForm(request.GET)
    else: 
        projects = Project.objects.all()
        projects, paginator, custom_range = pagePagination(request,projects, page)
        form = ProjectForm()
    
    context = {'projects': projects, 'form':form, 'paginator': paginator, 'custom_range': custom_range}
    return render(request,'projects_app/index.html',context)


def project(request, pk):
    project = Project.objects.get(pk = pk)
    if request.method == 'POST': 
        form = ReviewForm(request.POST)
        if form.is_valid(): 
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()
            project.getVoteCount 
            messages.success(request,'Your review was successfully added!')
            return HttpResponseRedirect(reverse('project', args=(project.id,)))
    form = ReviewForm()
    tags = project.tags.all()
    return render(request,'projects_app/project.html', { 
        'project' : project,
        'tags': tags,
        'form' : form,
    }) 

@login_required(login_url='login')
def create_project(request):
    if request.method == 'POST': 
        tags = request.POST['newTags'].replace(',',' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid(): 
            project = form.save()
            for tag in tags: 
                if tag not in project.tags.all(): 
                    new_tag = Tag.objects.create(name=tag)
                    project.tags.add(new_tag)
            project.save()
            return HttpResponseRedirect(reverse('index'))
        else: 
            return render(request,'projects_app/project_form.html', {
            'form': form,
        })

    form = ProjectForm()
    return render(request,'projects_app/project_form.html', {
        'form': form,

    })

@login_required(login_url='login')
def update_project(request, pk):
    project = Project.objects.get(id = pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST': 
        tags = request.POST['newTags'].replace(',',' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid(): 
            project_temp = form.save(commit=False)
            for tag in tags: 
                if tag not in project_temp.tags.all(): 
                    new_tag = Tag.objects.create(name=tag)
                    project.tags.add(new_tag)

            project_temp.save()
            return HttpResponseRedirect(reverse('index'))
        else: 
            return render(request,'projects_app/project_form.html', {
            'form': form,
            
        })

    return render(request,'projects_app/project_form.html', {
        'form': form,
    

    })

@login_required(login_url='login')
def delete_project(request, pk): 
    project = Project.objects.get(id=pk)
    if request.method == 'POST': 
        project.delete()
        return HttpResponseRedirect(reverse('index'))
    return render(request,'projects_app/delete.html',{
        'project' : project,
    } )


