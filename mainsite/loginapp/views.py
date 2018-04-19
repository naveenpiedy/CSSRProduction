from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from django.template.context_processors import csrf
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import password_reset_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.http import HttpResponse
from django.http import HttpResponseRedirect


def index(request):
    c = {}
    c.update(csrf(request))
    #print(c)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #print(request.POST)
        if "button_click" in request.POST:
            #print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                print('Testing')
                login(request, user)
                return redirect('/homeapp')
            else:
                messages.error(request, "Wrong email and password combination")
    return render(request, 'loginapp/base.html', c)


def signup(request):
    c = {}
    c.update(csrf(request))
    print(c)


def forget_password_step1(request):
    print(request)
    c = {}
    c.update(csrf(request))
    if request.method == 'POST' and "button_click" in request.POST:
        get_email = request.POST['email']
        users = User.objects.filter(email=get_email)
        if not users:
            messages.error(request,'This email address is not registed')
        else:
            list_id = []
            for user in users:
                list_id.append(user.id)
            max_id = max(list_id)
            spec_user = User.objects.get(id=max_id)
            current_site = get_current_site(request)
            message = render_to_string('loginapp/email.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(spec_user.pk)),
                'token': password_reset_token.make_token(spec_user),
            })
            mail_subject = 'CSSR Message: Reset your password.'
            to_email = get_email
            email_obj = EmailMessage(mail_subject, message, to=[to_email])
            email_obj.send()
            return HttpResponse('Please confirm your email address to complete the password reset')


    return render(request, 'loginapp/step1.html', c)


def reset(request, uidb64, token):
    print(request.POST)
    g = uidb64[1:]
    g = g.replace('\'', '')
    uid = force_text(urlsafe_base64_decode(str(g)))
    print(uid)
    try:
        uid = force_text(urlsafe_base64_decode(uidb64[1:].replace('\'', '')))
        print(uid)
        user = User.objects.get(pk=uid)
        print(uidb64)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and password_reset_token.check_token(user, token):
        if 'pass' in request.POST:
            if request.POST['pass'] and not request.POST['pass'].isspace():
                if request.POST['pass'] == request.POST['repass']:
                    user.is_active = True
                    user.set_password(request.POST['pass'])
                    user.save()
                    return redirect('/login/')
                else:
                    return HttpResponse("Password doesn't match")
        return render(request, 'loginapp/passwordReset.html')
    else:
        return HttpResponse("THHH")
