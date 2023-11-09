from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from csp.decorators import csp_exempt
import sweetify

from .models import Cv, Category
from .forms import CvForm


# return cv instances ordered by category
def cv(request):
    items = Cv.objects.all()
    category =  Category.objects.all()
    context = {
        'category': category,
        'items': items,
    }
    return render(request, "cv/cv.html", context)


# cv management page
@login_required
def cv_management(request):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    items = Cv.objects.all()
    category =  Category.objects.all()
    context = {
        'category': category,
        'items': items,
    }
    return render(request, "cv/cv_management.html", context)


# add cv item
@login_required
@csp_exempt
def add_cv(request):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = CvForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            sweetify.toast(request, 'Successfully added cv item', icon="success", timer=2000,
                            timerProgressBar=True)
            return redirect(reverse('cv_management'))
        else:
            sweetify.toast(request, 'Failed to add item. Please check your input.', icon="error", timer=2000,
                            timerProgressBar=True)
    else:
        form = CvForm()
    form = CvForm()
    template = 'cv/add_cv.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# edit cv instance
@login_required
@csp_exempt
def edit_cv(request, cv_id):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    cv_item = get_object_or_404(Cv, pk=cv_id)
    if request.method == 'POST':
        form = CvForm(request.POST, request.FILES, instance=cv_item)
        if form.is_valid():
            form.save()
            sweetify.toast(request, f'Successfully edited {cv_item.title}', icon="success", timer=2000,
                            timerProgressBar=True)
            return redirect(reverse('cv_management'))
        else:
            sweetify.toast(request, 'Failed to edit item. Please check your input.', icon="error", timer=2000,
                            timerProgressBar=True)
    else:
        form = CvForm(instance=cv_item)
        sweetify.toast(request, f'You are editing {cv_item.title}', icon="info", timer=2000,
                            timerProgressBar=True)
    template = 'cv/edit_cv.html'
    context = {
        'form': form,
        'cv': cv_item,
    }
    return render(request, template, context)


# delete cv instance
@login_required
def delete_cv(request, cv_id):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    cv_item = get_object_or_404(Cv, pk=cv_id)
    cv_item.delete()
    sweetify.toast(request, 'Successfully deleted item', icon="success", timer=2000,
                            timerProgressBar=True)
    return redirect(reverse('cv_management'))
