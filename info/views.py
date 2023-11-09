from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from csp.decorators import csp_exempt
import sweetify

from .models import Info, Category
from .forms import InfoForm


# return information instances with category news
def news(request):
    news = Info.objects.filter(
        category__name__icontains='news').order_by('-date')

    context = {
        'news': news,
    }
    return render(request, "info/news.html", context)


# return information instances with category texts
def texts(request):
    texts = Info.objects.filter(
        category__name__icontains='texts').order_by('-date')
    
    context = {
        'texts': texts,
    }
    return render(request, "info/texts.html", context)


# information management for admin
@login_required
def info_management(request):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('about'))
    category = Category.objects.all()
    items = Info.objects.all() 
    context = {
        'category': category,
        'items': items,
    }
    return render(request, "info/info_management.html", context)


# add information item
@login_required
@csp_exempt
def add_info(request):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = InfoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            sweetify.toast(request, 'Successfully added information', icon="success", timer=2000,
                            timerProgressBar=True)
            return redirect(reverse('info_management'))
        else:
            sweetify.toast(request, 'Failed to add item. Please check your input', icon="error", timer=2000,
                            timerProgressBar=True)
    else:
        sweetify.toast(request, 'Adding new info item', icon="info", timer=2000,
                            timerProgressBar=True)
        form = InfoForm()
    template = 'info/add_info.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


# edit information instance
@login_required
@csp_exempt
def edit_info(request, info_id):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    info = get_object_or_404(Info, pk=info_id)
    if request.method == 'POST':
        form = InfoForm(
            request.POST, request.FILES, instance=info)
        if form.is_valid():
            form.save()
            sweetify.toast(request, 'Successfully edited information', icon="success", timer=2000,
                            timerProgressBar=True)
            return redirect(reverse('info_management'))
        else:
            sweetify.toast(request, 'Failed to edit item. Please check your input', icon="error", timer=2000,
                            timerProgressBar=True)
    else:
        form = InfoForm(instance=info)
        sweetify.toast(request, f'You are editing {info.title}', icon="info", timer=2000,
                            timerProgressBar=True)
    template = 'info/edit_info.html'
    context = {
        'form': form,
        'info': info,
    }
    return render(request, template, context)


# delete information instance
@login_required
def delete_info(request, info_id):
    if not request.user.is_superuser:
        sweetify.toast(request, 'Only an Admin can access this page', icon="error", timer=2000,
                            timerProgressBar=True)
        return redirect(reverse('home'))
    info = get_object_or_404(Info, pk=info_id)
    info.delete()
    sweetify.toast(request, 'Successfully deleted information', icon="success", timer=2000,
                            timerProgressBar=True)
    return redirect(reverse('info_management'))
