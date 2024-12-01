from django.shortcuts import render
from .forms import PDFUploadForm
from django.http import HttpResponse
from .pdf_extraction_pipeline.run_pipeline import run_pipeline

def calculate():
    x = 1
    y = 2
    return x

# Create your views here.
def say_hello(request):
    x = calculate()
    return render(request, 'hello.html', {'name': 'Mosh'})

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']

            results = run_pipeline(pdf_file)

            return render(request, 'success.html', {'results': results})
    else:
        form = PDFUploadForm()
    return render(request, 'upload.html', {'form': form})