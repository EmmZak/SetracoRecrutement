from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import ProfileFile


@require_http_methods(["DELETE"])
def delete_file(request):
    file_id = request.GET.get('id')
    if file_id:
        ProfileFile.objects.filter(id=file_id).delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
