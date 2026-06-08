from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product
from .forms import ProductForm


def ping(request):
    return HttpResponse('OK', status=200)


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/index.html', {'object_list': products})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.full_clean()
                obj.save()
                messages.success(request, 'Товар успешно добавлен.')
                return redirect('index')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = ProductForm()
    return render(request, 'products/form.html', {'form': form})


def product_update(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=obj)
        if form.is_valid():
            try:
                updated = form.save(commit=False)
                updated.full_clean()
                updated.save()
                messages.success(request, 'Товар обновлён.')
                return redirect('index')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = ProductForm(instance=obj)
    return render(request, 'products/form.html', {'form': form, 'object': obj})


def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Товар удалён.')
        return redirect('index')
    return render(request, 'products/confirm_delete.html', {'object': obj})
