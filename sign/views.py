from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event
from sign.models import Guest
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    return render(request, 'index.html')


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            # response.set_cookie('user', username, 3600)
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


@login_required
def event_manage(request):
    Event_list = Event.objects.all()
    # username = request.COOKIES.get('user', '')
    username = request.session.get('user', '')
    return render(request, 'event_manage.html', {'user': username,
                                                 'events': Event_list})


@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Guest.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'user': username,
                                                 'events': event_list})


@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    contacts = paginatorFun(paginator, page)
    # print('event:{}'.format(guest_list))
    return render(request, 'guest_manage.html', {'user': username,
                                                 'guests': contacts})


@login_required
def search_guest(request):
    username = request.session.get('user', '')
    search_guest = request.GET.get('guest_name', '')
    guest_list = Guest.objects.filter(realname__contains=search_guest)
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    contacts = paginatorFun(paginator, page)
    # print('event:{}'.format(guest_list))
    return render(request, 'guest_manage.html', {'user': username,
                                                 'guests': contacts})


def paginatorFun(pagin, page):
    try:
        contacts = pagin.page(page)
    except PageNotAnInteger:
        contacts = pagin.page(1)
    except EmptyPage:
        contacts = pagin.page(pagin.num_pages)
    return contacts


@login_required
def sign_index(request, eid):
    guestallcount = Guest.objects.filter(event_id=eid).count()
    guestsignedcount = Guest.objects.filter(event_id=eid, sign=True).count()
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event,
                                               'guest_all': guestallcount,
                                               'guestsigned': guestsignedcount,
                                               })


@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print(phone)
    result = Guest.objects.filter(phone=phone)
    if result is None:
        return render(request, 'sign_index.html', {
            'event': event,
            'hint': 'phone error.'
        })

    result = Guest.objects.filter(phone=phone, event_id=eid)
    if result is None:
        return render(request, 'sign_index.html', {
            'event': event,
            'hint': 'event id or phone error.'
        })

    result = Guest.objects.get(phone=phone, event_id=eid)
    print('result:{}'.format(result))
    if result.sign is True:
        print('result.values:sign:{}'.format(result.sign))
        return render(request, 'sign_index.html', {
            'event': event,
            'hint': 'user has sign in.'
        })

    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {
            'event': event,
            'hint': 'sign in success!',
            'guest': result,
            'guest_all': Guest.objects.filter(event_id=eid).count(),
            'guestsigned': Guest.objects.filter(event_id=eid, sign=True).count(),

        })


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response
