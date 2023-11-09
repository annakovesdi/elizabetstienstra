from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from csp.decorators import csp_exempt
import sweetify

from .models import About
from .forms import AboutForm


# returns about page
def about(request):
    about_info = About.objects.all()

    context = {
        'about': about_info,
    }

    return render(request, "about/about.html", context)


# returns contact page
def contact(request):
    contact = About.objects.only('contact')

    context = {
        'contact': contact,
    }

    return render(request, "about/contact.html", context)



# edit about page - only one entry allowed
@login_required
@csp_exempt
def edit_about(request):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    existing_item = About.objects.first()
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES, instance=existing_item)
        if form.is_valid():
            if existing_item:
                existing_item.delete()
            form.save()
            sweetify.toast(request, 'Successfully edited the about section', icon="success", timer=2000,
                            timerProgressBar=True)
            return redirect(reverse('about'))
        else:
            sweetify.toast(request, 'Failed to edit work. Please check your input.', icon="error", timer=2000,
                            timerProgressBar=True)
    else:
        form = AboutForm(instance=existing_item)
        sweetify.toast(request, 'You are editing the about section', icon="info", timer=2000,
                            timerProgressBar=True)

    template = 'about/edit_about.html'
    context = {
        'form': form,
    }

    return render(request, template, context)