from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    oeuvre = Work.objects.all()
    commissions = oeuvre.filter(category__name='commissions')
    sculptures = oeuvre.filter(category__name='sculptures')
    context = {
        'commissions': commissions,
        'sculptures': sculptures,
    }
    return render(request, "oeuvre/oeuvre_management.html", context)


# add work
@login_required
def add_work(request):
    if not request.user.is_superuser:
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Succesfully added work')
            return redirect(reverse('oeuvre_management'))
        else:
            messages.error(request, 'Failed to add item. Please check your input.')
    else:
        form = WorkForm()
    form = WorkForm
    template = 'oeuvre/add_work.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# edit a work
@login_required
def edit_work(request, work_id):
    if not request.user.is_superuser:
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    work = get_object_or_404(Work, pk=work_id)
    images = Image.objects.filter(work__id=work_id)
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES, instance=work)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully edited work')
            return redirect(reverse('oeuvre_management'))
        else:
            messages.error(
                request, 'Failed to edit work. Please check your input.')
    else:
        form = WorkForm(instance=work)
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


# add an image
@login_required
def add_image(request, work_id):
    if not request.user.is_superuser:
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.work = Work.objects.get(id=work_id)
            image.save()
            messages.success(request, 'Succesfully added image')
            return redirect(reverse('edit_work', args=[work_id]))
        else:
            messages.error(request, 'Failed to add item. Please check your input.')


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