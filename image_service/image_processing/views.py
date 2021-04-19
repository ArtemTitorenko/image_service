from django.shortcuts import render, redirect

from .forms import ImageLoadForm, ImageResizeForm
from .models import Image
from . import services


def image_list(request):
    images = services.get_all_images()
    imgs = {img.image.name.split('/')[-1]: img for img in images}
    return render(request, 'image_list.html', {'images': imgs})


def upload_image(request):
    if request.method == 'POST':
        form = ImageLoadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data.get('image_file', None)
            image_url = form.cleaned_data.get('image_url', None)
            if image_file:
                image = services.save_image_by_file(image_file)
            else:
                image = services.save_image_by_url(image_url)
            return redirect('processing:resize_image', image_id=image.id)
    else:
        form = ImageLoadForm()
    return render(request, 'upload_image.html', {'form': form})


def resize_image(request, image_id: int):
    image = Image.objects.filter(id=image_id).first()
    image_name = image.image.name.split('/')[-1]

    if request.method == 'POST':
        form = ImageResizeForm(request.POST)
        if form.is_valid():
            width = form.cleaned_data['width']
            height = form.cleaned_data['height']
            image = services.resize_image(image, width, height)
    else:
        form = ImageResizeForm()

    context = {
        'form': form,
        'image_name': image_name,
        'image': image,
    }

    return render(request, 'resize_image.html', context)

