from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from csp.decorators import csp_exempt

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
        messages.error(request, 'Only an Admin can access this page')
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
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        imageform = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            o = form.save()
            files = request.FILES.getlist('images')
            for f in files:
                Image.objects.create(work=o, image=f)
            messages.success(request, 'Succesfully added work')
            return redirect(reverse('oeuvre_management'))
        else:
            messages.error(request, 'Failed to add item. Please check your input.')
    else:
        form = WorkForm()
        imageform = ImageForm()
    form = WorkForm
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
        messages.error(request, 'Only an Admin can access this page')
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
            messages.success(request, 'Successfully edited work')
            return redirect(reverse('oeuvre_management'))
        else:
            messages.error(
                request, 'Failed to edit work. Please check your input.')
    else:
        form = WorkForm(instance=work)
        imageform = ImageForm()
        messages.info(request, f'You are editing {work.title}')
    imageform = ImageForm()
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
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    image = get_object_or_404(Image, pk=image_id)
    image.delete()
    messages.success(request, 'Succesfully deleted work')
    return redirect(reverse('edit_work', args=[work_id]))


# delete work item
@login_required
def delete_work(request, work_id):
    if not request.user.is_superuser:
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    work = get_object_or_404(Work, pk=work_id)
    work.delete()
    messages.success(request, 'Succesfully deleted work')
    return redirect(reverse('oeuvre_management'))