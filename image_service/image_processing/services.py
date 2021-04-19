import os
import requests
import typing
import uuid

from django.conf import settings
from django.db.models import QuerySet
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image as PilImage

from .models import Image


def get_all_images() -> QuerySet:
    return Image.objects.all()


def get_image_by_id(id: int) -> Image:
    return Image.objects.get(id=id)


def save_image_by_file(image_file: InMemoryUploadedFile) -> Image:
    image = Image(image=image_file)
    image.save()
    return image


def save_image_by_url(url: str) -> None:
    response = requests.get(url)
    if response.ok:
        file_name = os.path.join(settings.IMAGE_DIR, url.split('/')[-1])
        _save_image_to_media_root(file_name, response.content)
        return _save_image_to_database(file_name)


def _save_image_to_media_root(
        name: str, file_data: typing.ByteString) -> None:
    with open(os.path.join(settings.MEDIA_ROOT, name), 'wb') as f:
        f.write(file_data)


def _save_image_to_database(name: str) -> Image:
    image = Image(image=name)
    image.save()
    return image


def resize_image(image: Image, width=None, height=None) -> Image:
    tmp_image = PilImage.open(image.image.path)
    if not width:
        tmp_image = _resize_image_by_fixed_height(tmp_image, height)
    elif not height:
        tmp_image = _resize_image_by_fixed_width(tmp_image, width)
    else:
        tmp_image = tmp_image.resize((width, height))

    image_format = image.image.name.split('.')[-1]
    random_name = f'{uuid.uuid4()}.{image_format}'

    image_name = os.path.join(settings.IMAGE_DIR,
                              settings.TMP_IMAGE_DIR,
                              random_name)

    tmp_image_path = os.path.join(settings.MEDIA_ROOT, image_name)
    tmp_image.save(tmp_image_path)

    return Image(image=image_name)


def _resize_image_by_fixed_width(image: PilImage, width: int) -> PilImage:
    width_percent = (width / float(image.size[0]))
    height_size = int((float(image.size[1]) * float(width_percent)))
    return image.resize((width, height_size), PilImage.NEAREST)


def _resize_image_by_fixed_height(image: PilImage, height: int) -> PilImage:
    height_percent = (height / float(image.size[1]))
    width_size = int((float(image.size[0]) * float(height_percent)))
    return image.resize((width_size, height), PilImage.NEAREST)

