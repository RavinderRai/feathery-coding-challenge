from django.shortcuts import render
from .forms import PDFUploadForm
from django.http import HttpResponse
from .pdf_extraction_pipeline.run_pipeline import run_pipeline


def upload_pdf(request) -> HttpResponse:
    """
    Handle PDF upload and process it through the extraction pipeline.
    """
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']

            results = run_pipeline(pdf_file)

            return render(request, 'success.html', {'results': results})
    else:
        form = PDFUploadForm()
    return render(request, 'upload.html', {'form': form})