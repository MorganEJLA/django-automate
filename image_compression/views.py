from django.shortcuts import render, redirect
from .forms import CompressImageForm
from PIL import Image
import io
from django.http import HttpResponse

# Create your views here.
def compress(request):
    user = request.user
    if request.method == 'POST':
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data['original_img']
            quality = form.cleaned_data['quality']

            compressed_img = form.save(commit=False)
            compressed_img.user = user

            # perform compression
            img = Image.open(original_img)
            output_format = img.format
            buffer = io.BytesIO()
            img.save(buffer, format=output_format, quality=quality)
            print('cursor position at the beginning=>', buffer.tell())


            img.save(buffer, format='JPEG', quality=quality)
            print('cursor position after image compression=>', buffer.tell())
            buffer.seek(0)
            # save the compressed image inside the model
            compressed_img.compressed_img.save(
                f'compressed_{original_img}', buffer
            )
            # Automatically download the compressed file
            response = HttpResponse(buffer.getvalue(), content_type=f'img/{output_format.lower()}')
            response['Content-Disposition'] = f'attachment;filename=compressed_{original_img}'
            return response
            # return redirect('compress')




    else:
        form = CompressImageForm()
        context = {
            'form':form,
        }
        return render(request, 'image_compression/compress.html', context)
