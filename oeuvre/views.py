from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from csp.decorators import csp_exempt
import sweetify

from .models import Work, Category, Image
from .forms import WorkForm, CategoryForm, ImageForm



def oeuvre(request):
    oeuvre = Work.objects.all()
    category = None

    if request.GET:
        if 'category' in request.GET:
            category = request.GET['category'].split(',')
            oeuvre = oeuvre.filter(category__name__in=category)
            category = Category.objects.filter(name__in=category)
            images = Image.objects.filter(work__in=oeuvre)
            

    context = {
        'oeuvre': oeuvre,
        'category': category,
        'images': images,
    }
    return render(request, "oeuvre/oeuvre.html", context)


# oeuvre management
@login_required
def oeuvre_management(request):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    items = Work.objects.all()
    category =  Category.objects.all()
    context = {
        'category': category,
        'items': items,
    }
    return render(request, "oeuvre/oeuvre_management.html", context)


# add work
@login_required
@csp_exempt
def add_work(request):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        imageform = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            o = form.save()
            files = request.FILES.getlist('images')
            for f in files:
                Image.objects.create(work=o, image=f)
            sweetify.toast(request, 'Succesfully added work', icon="success", timer=2000,
                            timerProgressBar=True)
            return redirect(reverse('oeuvre_management'))
        else:
            sweetify.toast(request, 'Failed to add item. Please check your input', icon="error", timer=2000,
                            timerProgressBar=True)
    else:
        sweetify.toast(request, 'Adding new work', icon="info", timer=2000,
                            timerProgressBar=True)
        form = WorkForm()
        imageform = ImageForm()
    template = 'oeuvre/add_work.html'
    context = {
        'form': form,
        'imageform': imageform,
    }
    return render(request, template, context)


# edit a work
@login_required
@csp_exempt
def edit_work(request, work_id):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    work = get_object_or_404(Work, pk=work_id)
    images = Image.objects.filter(work__id=work_id)
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES, instance=work)
        imageform = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            o = form.save()
            files = request.FILES.getlist('images')
            for f in files:
                Image.objects.create(work=o, image=f)
            sweetify.toast(request, f'Succesfully edited {work.title}', icon="success", timer=2000,
                            timerProgressBar=True)
            return redirect(reverse('oeuvre_management'))
        else:
            sweetify.toast(request, 'Failed to edit item. Please check your input', icon="error", timer=2000,
                            timerProgressBar=True)
    else:
        form = WorkForm(instance=work)
        imageform = ImageForm()
        sweetify.toast(request, f'You are editing {work.title}', icon="info", timer=2000,
                            timerProgressBar=True)
    template = 'oeuvre/edit_work.html'
    context = {
        'form': form,
        'work': work,
        'images': images,
        'imageform': imageform,
    }
    return render(request, template, context)


# delete image item
@login_required
def delete_image(request, image_id, work_id):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    image = get_object_or_404(Image, pk=image_id)
    image.delete()
    sweetify.toast(request, 'Succesfully deleted image', icon="success", timer=2000,
                            timerProgressBar=True)
    return redirect(reverse('edit_work', args=[work_id]))


# delete work item
@login_required
def delete_work(request, work_id):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    work = get_object_or_404(Work, pk=work_id)
    work.delete()
    sweetify.toast(request, 'Succesfully deleted work', icon="success", timer=2000,
                           timerProgressBar=True)
    return redirect(reverse('oeuvre_management'))