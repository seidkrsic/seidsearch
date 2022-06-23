
from projects_app.models import Tag
from django.db.models import Q 
from projects_app.forms import ProjectForm 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from projects_app.models import Project 

def searchProjects(request): 
    search_query = request.GET['title']
    tags = Tag.objects.filter(name__icontains = search_query)
    projects = Project.objects.distinct().filter(
        Q(title__icontains = search_query) | 
        Q(description__icontains = search_query) | 
        Q(owner__name__icontains = search_query) | 
        Q(tags__in=tags)
    )
    form = ProjectForm(request.GET)
    return projects, form 


def pagePagination(request,projects, page): 
    paginator = Paginator(projects, 2)
    try: 
        projects = paginator.page(page)
    except PageNotAnInteger: 
        projects = paginator.page(1)
    except EmptyPage: 
        projects = paginator.page(paginator.num_pages)
    
    if page: 
        left_index = int(page) - 2
        if left_index < 1: 
            left_index = 1 
        
        right_index = int(page) + 3

        if right_index > paginator.num_pages:
            right_index = paginator.num_pages + 1 

        custom_range = range(left_index,right_index)
    else: 
        custom_range = range(1,3)
    form = ProjectForm()
    return projects, paginator, custom_range