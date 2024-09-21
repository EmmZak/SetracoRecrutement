from django.http import JsonResponse
from profiles.serializers import ProfileSerializer
from .models import Profile, Comment, ProfileFile
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
import os
from django.core.serializers import serialize
import csv
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

@login_required
@permission_required('profiles.delete_comment')
@require_http_methods(["DELETE"])
def delete_comment(request):
    com_id = request.GET.get('id')
    print("deleting comment: ", com_id)
    if com_id:
        Comment.objects.filter(id=com_id).delete()
        print("returning success")
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

@login_required
@permission_required('profiles.delete_profilefile')
@require_http_methods(["DELETE"])
def delete_file(request):
    file_id = request.GET.get('id')
    if file_id:
        ProfileFile.objects.filter(id=file_id).delete()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


@login_required
def export_profile_pdf(request):
    profile_id = request.GET.get("id")
    profile = Profile.objects.get(id=profile_id)

    # Create a HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{profile.name}_{profile.surname}.pdf"'

    # Create the PDF object
    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Helper function for page footer
    def add_footer(page_num):
        pdf.setFont("Helvetica", 10)
        pdf.setFillColor(colors.grey)
        pdf.drawString(100, 20, f"Page {page_num}")

    # Page number counter
    page_num = 1

    # Add profile title
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(100, height - 60,
                   f"Profil de {profile.name} {profile.surname}")

    pdf.setLineWidth(1)
    pdf.setStrokeColor(colors.black)
    pdf.line(100, height - 80, width - 100, height - 80)  # Horizontal line

    # Set standard font for profile info
    pdf.setFont("Helvetica", 12)

    # Draw profile details
    pdf.drawString(100, height - 120, "Informations Personnelles")
    pdf.setFont("Helvetica", 11)
    y_position = height - 140

    profile_details = [
        ("Email", profile.email),
        ("Numéro", profile.number),
        ("Ville", profile.town),
        ("Compétences", ', '.join(
            [skill.name for skill in profile.skills.all()])),
        ("Diplômes", profile.diplomas),
        ("Date de création", profile.creation_date.strftime('%d/%m/%Y %H:%M:%S')),
        ("Date de mise à jour", profile.update_date.strftime('%d/%m/%Y %H:%M:%S')),
        ("Etat candidature", getattr(profile.state, 'name', "Inconnu"))
    ]

    for label, value in profile_details:
        pdf.drawString(120, y_position, f"{label}: {value}")
        y_position -= 20

    # Add comments section
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(100, y_position, "Commentaires:")
    y_position -= 20
    pdf.setFont("Helvetica", 11)
    for comment in profile.comments.all():
        pdf.drawString(120, y_position,
                       f"{comment.user.username}: {comment.text}")
        y_position -= 20
        if y_position < 50:
            add_footer(page_num)
            pdf.showPage()
            page_num += 1
            y_position = height - 100
            pdf.setFont("Helvetica", 11)

    # Add a new page for each file
    for profile_file in profile.files.all():
        add_footer(page_num)
        pdf.showPage()  # New page for each file
        page_num += 1

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(100, height - 100, f"Fichier: {profile_file.file.name}")

        # Check if the file is an image and display it
        file_path = profile_file.file.path
        if os.path.exists(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = ImageReader(file_path)
                img_width, img_height = img.getSize()
                aspect_ratio = img_height / img_width
                # Set max width for image
                img_display_width = min(400, width - 200)
                img_display_height = img_display_width * aspect_ratio
                pdf.drawImage(img, 100, height - 200 - img_display_height,
                              width=img_display_width, height=img_display_height)
            except Exception as e:
                pdf.drawString(100, height - 130, f"Unable to load image: {e}")
        else:
            pdf.drawString(100, height - 130, "Non-image file (not displayed)")

    # Add footer to last page
    add_footer(page_num)

    # Save PDF
    pdf.save()

    return response


@login_required
def export_profiles_csv(request):
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search', '')
    # Filter by skills (assuming the skill filter is a comma-separated list of skill IDs)
    skill_filter = request.GET.get('skills', '')
    state_filter = request.GET.get('states', '')

    profiles = Profile.objects.all()
    if search_value:
        profiles = profiles.filter(
            Q(name__icontains=search_value) |
            Q(surname__icontains=search_value) |
            Q(email__icontains=search_value) |
            Q(number__icontains=search_value)
        )

    if skill_filter:
        skill_ids = skill_filter.split(',')
        profiles = profiles.filter(skills__id__in=skill_ids).distinct()

    if state_filter:
        states = state_filter.split(',')
        print("states: ", states)
        profiles = profiles.filter(state__in=states)

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="profiles.csv"'

    writer = csv.writer(response)

    # Write the header row
    writer.writerow([
        'Nom', 'Prénom', 'Email', 'Numéro', 'Ville', 'Compétences', 'Diplômes',
        'Date de création', 'Date de mise à jour', 'État', 'Commentaires'
    ])

    # Write the data rows
    for profile in profiles:
        # Get all skills as a comma-separated string
        skills = ', '.join([skill.name for skill in profile.skills.all()])

        # Get all comments as a combined string
        comments = '; '.join(
            [f"{comment.user.username}: {comment.text}" for comment in profile.comments.all()])

        state = getattr(profile.state, 'name', "Inconnu")
        creation_date = profile.creation_date.strftime('%d/%m/%Y %H:%M:%S')
        update_date = profile.update_date.strftime('%d/%m/%Y %H:%M:%S')

        writer.writerow([
            profile.name, profile.surname, profile.email, profile.number, profile.town,
            skills, profile.diplomas, creation_date, update_date, state, comments
        ])

    return response


@login_required
@permission_required('profiles.add_profile')
@require_http_methods(["GET"])
def check_profile(request):
    data = request.GET
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    number = data.get('number')

    result = {}
    print("simi check", name, surname, email, number)
    if Profile.objects.filter(name=name).exists():
        # result['name'] = True
        pass
    if Profile.objects.filter(surname=surname).exists():
        # result['surname'] = True
        pass
    if Profile.objects.filter(email=email).exists():
        result['email'] = True
    # Assuming 'number' is a field in Profile
    if Profile.objects.filter(number=number).exists():
        result['number'] = True

    return JsonResponse(result)

@permission_required('profiles.view_profile')
@login_required
def profiles_data(request):
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search', '')
    # comma-separated list of IDs
    skill_filter = request.GET.get('skills', '')
    state_filter = request.GET.get('states', '')

    profiles = Profile.objects.all()
    if search_value:
        profiles = profiles.filter(
            Q(name__icontains=search_value) |
            Q(surname__icontains=search_value) |
            Q(email__icontains=search_value) |
            Q(number__icontains=search_value) |
            Q(town__icontains=search_value)
        )

    if skill_filter:
        skill_ids = skill_filter.split(',')
        profiles = profiles.filter(skills__id__in=skill_ids).distinct()

    if state_filter:
        state_ids = state_filter.split(',')
        profiles = profiles.filter(state__id__in=state_ids).distinct()

    paginator = Paginator(profiles, length)
    profiles_page = paginator.get_page(start // length + 1)

    serializer = ProfileSerializer(profiles_page, many=True)

    response = {
        # 'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'profiles': serializer.data,
    }

    return JsonResponse(response, encoder=DjangoJSONEncoder)
