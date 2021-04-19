from django import forms


class ImageLoadForm(forms.Form):
    image_url = forms.URLField(label='Ссылка', required=False)
    image_file = forms.ImageField(label='Файл', required=False)

    def clean(self):
        cleaned_data = super().clean()
        image_url = cleaned_data.get('image_url')
        image_file = cleaned_data.get('image_file')

        if image_url and image_file:
            raise forms.ValidationError(
                    'Нельзя отправлять сразу два изображения'
            )
        elif not image_url and not image_file:
            raise forms.ValidationError(
                    'Нужно загрузить изображение'
            )


class ImageResizeForm(forms.Form):
    width = forms.IntegerField(min_value=1,
                               label='Ширина',
                               required=False)
    height = forms.IntegerField(min_value=1,
                                label='Высота',
                                required=False)

    def clean(self):
        cleaned_data = super().clean()
        width = cleaned_data.get('width')
        height = cleaned_data.get('height')

        if not width and not height:
            raise forms.ValidationError(
                    'Нужно задать хотя бы один параметр'
            )

