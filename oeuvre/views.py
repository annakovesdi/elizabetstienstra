from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Work, Category
from .forms import WorkForm, CategoryForm


def oeuvre(request):
    oeuvre = Work.objects.all()
    category = None

    if request.GET:
        if 'category' in request.GET:
            category = request.GET['category'].split(',')
            oeuvre = oeuvre.filter(category__name__in=category).order_by('-date')
            category = Category.objects.filter(name__in=category)

    context = {
        'oeuvre': oeuvre,
        'category': category,
    }
    return render(request, "oeuvre/oeuvre.html", context)


# return instance of work
def work_detail(request, work_id):
    work = get_object_or_404(Work, pk=work_id)
    context = {
        'work': work,
    }
    return render(request, context)


# oeuvre management
@login_required
def oeuvre_management(request):
    if not request.user.is_superuser:
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('home'))
    oeuvre_items = Work.objects.all()
    categories = Category.objects.all()
    context = {
        'oeuvre': oeuvre_items,
        'categories': categories,
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
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES, instance=work)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully edited work')
            return redirect(reverse('work_detail', args=[work.id]))
        else:
            messages.error(
                request, 'Failed to edit work. Please check your input.')
    else:
        form = WorkForm(instance=work)
        messages.info(request, f'You are editing {work.title}')

    template = 'oeuvre/edit_work.html'
    context = {
        'form': form,
        'work': work,
    }

    return render(request, template, context)


# delete item
@login_required
def delete_work(request, work_id):
    if not request.user.is_superuser:
        messages.error(request, 'Only an Admin can access this page')
        return redirect(reverse('about'))
    work = get_object_or_404(Work, pk=work_id)
    work.delete()
    messages.success(request, 'Succesfully deleted work')
    return redirect(reverse('oeuvre_management'))