from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
def about(request):
    contact = About.objects.only('contact')

    context = {
        'contact': contact,
    }

    return render(request, "about/contact.html", context)



# edit about page - only one entry allowed
@login_required
def edit_about(request):
    if not request.user.is_superuser:
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    existing_item = About.objects.first()
    if request.method == 'POST':
        form = AboutForm(request.POST, request.FILES, instance=existing_item)
        if form.is_valid():
            existing_item.delete()
            form.save()
            messages.success(request, 'Successfully edited item')
            return redirect(reverse('about'))
        else:
            messages.error(
                request, 'Failed to edit work. Please check your input.')
    else:
        form = AboutForm(instance=existing_item)
        messages.info(request, 'You are editing the about section')

    template = 'about/edit_about.html'
    context = {
        'form': form,
    }

    return render(request, template, context)