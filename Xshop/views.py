from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import ContactForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def home_page(request):
    context = {
        "title" : "contact",
        "content" : "welcome to the contact page",
    }
    if request.user.is_authenticated:
        context["premium_content"] = "you are premium"
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"contact",
        "content":"welcome to the contact page",
        "form":contact_form,

    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message" : "thank you for the submission"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')


    # if request.method == "POST":
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))
    return render(request, 'contact/view.html', context)



