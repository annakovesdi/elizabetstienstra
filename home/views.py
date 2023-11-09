from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import sweetify

from .models import Home
from .forms import HomeForm


# return homepage
def index(request):
    image = Home.objects.all()
    context = {
        'image': image,
    }
    return render(request, "home/home.html", context)


# edit home data, only one instance allowed
@login_required
def home_management(request):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    existing_item = Home.objects.first()
    if request.method == 'POST':
        form = HomeForm(request.POST, request.FILES, instance=existing_item)
        if form.is_valid():
            if existing_item:
                existing_item.delete()
            form.save()
            sweetify.toast(request, 'Successfully edited Home', icon="success", timer=2000,
                            timerProgressBar=True)
            return redirect(reverse('home'))
        else:
            sweetify.toast(request, 'Failed to edit Home. Please check your input', icon="error", timer=2000,
                            timerProgressBar=True)
    else:
        sweetify.toast(request, 'Editing Home section', icon="info", timer=2000,
                            timerProgressBar=True)
        form = HomeForm(instance=existing_item)
    template = 'home/home_management.html'
    context = {
        'form': form,
        'image': existing_item,
    }
    return render(request, template, context)
