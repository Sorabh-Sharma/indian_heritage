import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST
from .models import HeritageItem
from .forms import HeritageItemForm


def landing(request):
    return render(request, 'landing.html')


def home(request):
    items = HeritageItem.objects.all()

    # --- Search ---
    query = request.GET.get('q', '').strip()
    if query:
        items = items.filter(
            Q(title__icontains=query) |
            Q(region__icontains=query) |
            Q(description__icontains=query)
        )

    # --- Category filter ---
    category = request.GET.get('category', '').strip()
    if category:
        items = items.filter(category__iexact=category)

    # All unique categories for the filter tags
    all_categories = HeritageItem.objects.values_list('category', flat=True).distinct()

    # --- Map data: only items with valid coordinates ---
    items = list(items)
    map_items = []
    for item in items:
        lat = getattr(item, 'latitude', None)
        lng = getattr(item, 'longitude', None)
        if lat is not None and lng is not None:
            map_items.append({
                'id': str(item.pk),
                'title': item.title,
                'region': item.region,
                'latitude': lat,
                'longitude': lng,
                'url': reverse('item_detail', kwargs={'pk': str(item.pk)}),
            })

    return render(request, 'home.html', {
        'items': items,
        'query': query,
        'category': category,
        'all_categories': all_categories,
        'map_data': json.dumps(map_items),
        'mapbox_token': getattr(settings, 'MAPBOX_ACCESS_TOKEN', ''),
    })


# ═══════════════════════════════════════════════════════════════
# AUTHENTICATION VIEWS
# ═══════════════════════════════════════════════════════════════

def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to IndiaHeritage, {user.username}!")
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@require_POST
def logout_user(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


# ═══════════════════════════════════════════════════════════════
# HERITAGE ITEM CRUD VIEWS
# ═══════════════════════════════════════════════════════════════

@login_required
def add_item(request):
    if request.method == 'POST':
        form = HeritageItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.author = request.user
            item.save()
            messages.success(request, f'"{item.title}" was added successfully!')
            return redirect('home')
    else:
        form = HeritageItemForm()
    return render(request, 'add_item.html', {'form': form})


def item_detail(request, pk):
    item = get_object_or_404(HeritageItem, pk=pk)
    return render(request, 'item_detail.html', {'item': item})


@login_required
def edit_item(request, pk):
    item = get_object_or_404(HeritageItem, pk=pk)

    # Verify ownership
    if item.author and request.user != item.author:
        return HttpResponseForbidden("You do not have permission to edit this heritage item.")

    if request.method == 'POST':
        form = HeritageItemForm(request.POST, instance=item)
        if form.is_valid():
            saved_item = form.save(commit=False)
            if not saved_item.author:
                saved_item.author = request.user
            saved_item.save()
            messages.success(request, f'"{saved_item.title}" was updated successfully!')
            return redirect('item_detail', pk=pk)
    else:
        form = HeritageItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form, 'item': item})


@login_required
def delete_item(request, pk):
    item = get_object_or_404(HeritageItem, pk=pk)

    # Verify ownership
    if item.author and request.user != item.author:
        return HttpResponseForbidden("You do not have permission to delete this heritage item.")

    if request.method == 'POST':
        title = item.title
        item.delete()
        messages.success(request, f'"{title}" was deleted.')
        return redirect('home')
    return render(request, 'confirm_delete.html', {'item': item})
