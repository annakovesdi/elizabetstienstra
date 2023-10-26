from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Cv, Category
from .forms import CvForm


# return cv instances ordered by category
def cv(request):
    cv = Cv.objects.all()
    """
    bio = Cv.objects.filter(category__name__icontains='bio')
    solo_exhibitions = Cv.objects.filter(
        category__name__icontains='solo_exhibitions')
    group_exhibitions = Cv.objects.filter(
        category__name__icontains='group_exhibitions')
    commissions = Cv.objects.filter(
        category__name__icontains='commissions')
    collections = Cv.objects.filter(
        category__name__icontains='collections')
        """
    context = {
        """
        'bio': bio,
        'solo_exhibitions': solo_exhibitions,
        'group_exhibitions': group_exhibitions,
        'commissions': commissions,
        'collections': collections,
        """
        'cv': cv,
    }
    return render(request, "cv/cv.html", context)


# cv management page
@login_required
def cv_management(request):
    if not request.user.is_superuser:
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    cv_item = Cv.objects.all()
    context = {
        'cv': cv_item,
    }
    return render(request, "cv/cv_management.html", context)


# add cv item
@login_required
def add_cv(request):
    if not request.user.is_superuser:
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = CvForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Succesfully added information')
            return redirect(reverse('cv_management'))
        else:
            messages.error(request,
                           'Failed to add item. Please check your input.')
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
def edit_cv(request, cv_id):
    if not request.user.is_superuser:
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    cv_item = get_object_or_404(Cv, pk=cv_id)
    if request.method == 'POST':
        form = CvForm(request.POST, request.FILES, instance=cv_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully edited information')
            return redirect(reverse('cv_management'))
        else:
            messages.error(
                request, 'Failed to edit work. Please check your input.')
    else:
        form = CvForm(instance=cv_item)
        messages.info(request, f'You are editing {cv_item.category}')

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
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    cv_item = get_object_or_404(Cv, pk=cv_id)
    cv_item.delete()
    messages.success(request, 'Succesfully deleted')
    return redirect(reverse('cv_management'))
