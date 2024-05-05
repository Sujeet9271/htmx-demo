import json
import time
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect

from accounts.forms import EventForm, TicketsForm
from accounts.models import Event, Users, Tickets, Menu, SubMenu
# Create your views here.


def auth_login(request):
    context={}
    if request.user.is_authenticated:
        return redirect('accounts:index')
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            if request.htmx:
                return HttpResponseClientRedirect(redirect_to='/')
            return redirect('accounts:index')
        messages.error(request,message='Username or Password is incorrect')
        if request.htmx:
            response =  render(request,'accounts/htmx/login_form.html',context)
            response['HX-Reswap']='innerHTML'
            response['HX-Retarget']='.login'
            return response
    return render(request,'accounts/login.html',context)


@login_required()
def index(request):
    context={}
    if request.htmx:
        time.sleep(5)
        return render(request,'welcome.html',context)
    return render(request,'index.html', context)

@login_required()
def log_out(request):
    logout(request)
    return redirect('accounts:index')

@login_required()
@require_http_methods(['GET','POST'])
def create_event(request):
    if request.method=='POST':
        form = EventForm(data=request.POST)
        if form.is_valid():
            event = form.save()
            response = render(request,'events/event.html',{'event':event})
            response['HX-Trigger']="clearForm"
            return response
        response = render(request,'events/create_event.html',{'form':form})
        response['HX-Retarget']="#event_form_div"
        response['HX-Reswap']="innerHTML"
        return response
    return render(request,'events/create_event.html',{'form':EventForm()})


@login_required()
@require_http_methods(['GET','POST'])
def edit_event(request,id):
    event = Event.objects.filter(id=id).first()
    form = EventForm(data=request.POST or None, instance=event)
    if request.method=='POST':
        if form.is_valid():
            event = form.save()
            response = render(request,'events/event.html',{'event':event,'edited':True, 'form':EventForm()})
            return response
        response = render(request,'events/edit_event.html',{'form':form})
        response['HX-Retarget']="#event_form_div"
        response['HX-Reswap']="innerHTML"
        return response
    return render(request,'events/edit_event.html',{'form':form})


@login_required()
@require_http_methods(['DELETE'])
def delete_event(request,id):
    Event.objects.filter(id=id).delete()
    response = HttpResponse(status=200)
    response['HX-Trigger']='get_all_events'
    return response

@login_required()
@require_http_methods(['GET'])
def get_all_events(request):
    context={}
    if request.htmx:
        events = Event.objects.all()
        context['events']=events
        return render(request,'events/all.html',context)
    form = EventForm()
    context['form'] = form
    return render(request,'events/index.html',context)




@login_required()
@require_http_methods(['GET'])
def get_all_users(request):
    context={}
    if request.htmx:
        search = request.GET.get('search')
        if search:
            qs = Users.objects.filter(name__icontains=search)
        else:
            qs = Users.objects.all()
        limit=10
        page = request.GET.get('page',1)
        limit = request.GET.get('limit',50)
        paginator = Paginator(qs, limit)
        page_obj = paginator.get_page(page)
        context['users']=page_obj
        time.sleep(2)
        return render(request,'scroll/all.html',context)
    form = EventForm()
    context['form'] = form
    return render(request,'scroll/index.html',context)

@login_required()
def tickets(request):
    context={}
    form = TicketsForm(request.POST or None)
    if request.method=='POST':
        if form.is_valid():
            ticket = form.save()
            response = HttpResponse(status=200)
            response['HX-Trigger']=json.dumps({"loadTickets":{"level":"info"},"clearForm":{'level':'info'}})
            return response
    context['form'] = form
    return render(request,'chain/index.html',context)


@login_required()
def get_menu(request):
    project_id = request.GET.get('project_id')
    menus = Menu.objects.filter(project_id_id=project_id)
    return render(request,'chain/menu.html',{'menus':menus})

@login_required()
def get_sub_menu(request):
    project_id = request.GET.get('project_id')
    menu_id = request.GET.get('menu_id')
    sub_menus = SubMenu.objects.filter(project_id_id=project_id,menu_id_id=menu_id)
    return render(request,'chain/sub_menu.html',{'sub_menus':sub_menus})


@login_required()
def get_all_tickets(request):
    context={}
    tickets = Tickets.objects.all()
    context['tickets'] = tickets
    return render(request,'chain/tickets.html',context)