from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    existing_item = Home.objects.first()
    if request.method == 'POST':
        form = HomeForm(request.POST, request.FILES, instance=existing_item)
        if form.is_valid():
            existing_item.delete()
            form.save()
            messages.success(request, 'Succesfully added work')
            return redirect(reverse('home'))
        else:
            messages.error(
                request, 'Failed to add item. Please check your input.')
    else:
        form = HomeForm(instance=existing_item)
    form = HomeForm(instance=existing_item)
    template = 'home/home_management.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
