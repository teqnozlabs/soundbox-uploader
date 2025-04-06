import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseForbidden
from django.core.files.base import ContentFile
from django.core.files.storage import storages
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

@csrf_exempt  # Since you're not using CSRF tokens in Postman or Flutter
def upload_file(request):
    admin_key = request.headers.get("X-Admin-Key")
    expected_key = os.getenv("ADMIN_SECRET_KEY")

    if admin_key != expected_key:
        return HttpResponseForbidden("Invalid admin key")

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        storage = storages["default"]
        path = storage.save(uploaded_file.name, ContentFile(uploaded_file.read()))
        file_url = storage.url(path)

        return JsonResponse({
            'message': 'File uploaded successfully',
            'file_url': file_url
        })

    return JsonResponse({'error': 'No file uploaded or wrong method'}, status=400)
