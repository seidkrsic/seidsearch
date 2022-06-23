

from user_app.models import Skill, Profile, Chat 
from user_app.forms import DeveloperForm 
from django.db.models import Q 

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 



def searchInbox(request): 
    recepient = request.user.profile
    chat_rooms = Chat.objects.filter(
        Q(recepient=recepient) | 
        Q(sender=recepient)
        # here update distinct on field unique_id and that's it. Only works for POSTGRESQL
    ).distinct()
    return chat_rooms 



def InboxPagination(request,chat_rooms, page): 
    paginator = Paginator(chat_rooms,3)
    try: 
        chat_rooms = paginator.page(page)
    except PageNotAnInteger: 
        chat_rooms = paginator.page(1)
    except EmptyPage: 
        chat_rooms = paginator.page(paginator.num_pages)

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

    return chat_rooms, paginator, custom_range



def pagePagination(request,profiles, page): 
    paginator = Paginator(profiles, 2)
    try: 
        profiles = paginator.page(page)
    except PageNotAnInteger: 
        profiles = paginator.page(1)
    except EmptyPage: 
        profiles = paginator.page(paginator.num_pages)
    
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
    # form = DeveloperForm()
    return profiles, paginator, custom_range


def searchProfiles(request): 
    search_query = request.GET.get('name')
    skills = Skill.objects.filter(name__icontains = search_query)
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains = search_query) | 
        Q(short_intro__icontains = search_query) | 
        Q(skill__in = skills)
    
    )
    form = DeveloperForm(request.GET)
    return profiles, form 