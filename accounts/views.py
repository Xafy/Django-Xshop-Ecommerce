from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from .forms import  SigninForm, SignupForm, GuestForm
from .signals import user_logged_in
from accounts.models import GuestEmail
from django.contrib.auth import authenticate, login
from django.conf import settings

User = settings.AUTH_USER_MODEL

def guest_signup_view(request):
    form = GuestForm(request.POST or None)
    context = {
        'form' : form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/signup/")
    return redirect("/signup/")

class SigninView(FormView):
    form_class = SigninForm
    success_url = '/'
    template_name = 'accounts/signin.html'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance = user, request = request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        return super(SigninView, self).form_invalid(form)



class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = '/signin/'

# def signup_page(request):
    # form = SignupForm(request.POST or None)
    # context = {
    #     "form" : form
    # }

    # if form.is_valid():
    #     form.save()
    # return render(request, 'accounts/signup.html', context)

# def signin_page(request):
#     form = SigninForm(request.POST or None)
#     context = {
#         'form' : form
#     }
#     # print('user is logged in')
#     # print(request.user.is_authenticated)
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         print(form.cleaned_data)
#         username = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect("/")
#         else:
#             print('error')
    
#     return render(request, 'accounts/signin.html', context)