from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import ProfileFile


@require_POST
def delete_file(request):
    file_id = request.POST.get('id')
    print("file_id: ", file_id)
    if file_id:
        ProfileFile.objects.filter(id=file_id).delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
