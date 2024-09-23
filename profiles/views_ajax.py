import csv
import os

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas

from SetracoRecrutement.logger import Logger
from profiles.serializers import ProfileSerializer

from .models import Comment, Profile, ProfileFile

logger = Logger('profiles_ajax')


@login_required
@permission_required('profiles.delete_comment')
@require_http_methods(["DELETE"])
def delete_comment(request):
    com_id = request.GET.get('id')
    logger.info(f"Deleting comment by id: {com_id}", request=request)
    try:
        if com_id:
            Comment.objects.filter(id=com_id).delete()
            print("returning success")
            return JsonResponse({'success': True})
    except Exception as e:
        logger.error(
            f"Error deleting comment by id: {com_id} {e}", request=request)

    return JsonResponse({'success': False})


@login_required
@permission_required('profiles.delete_profilefile')
@require_http_methods(["DELETE"])
def delete_file(request):
    file_id = request.GET.get('id')
    logger.info(f"Deleting file by id: {file_id}", request=request)
    try:
        if file_id:
            ProfileFile.objects.filter(id=file_id).delete()
            return JsonResponse({'success': True})
    except Exception as e:
        logger.error(
            f"Error deleting file by id: {file_id} {e}", request=request)

    return JsonResponse({'success': False})


@login_required
def export_profile_pdf(request):
    profile_id = request.GET.get("id")
    logger.info(f"Exporting profile by id: {profile_id}", request=request)

    try:
        profile = Profile.objects.get(id=profile_id)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{profile.name}_{profile.surname}.pdf"'

        pdf = canvas.Canvas(response, pagesize=A4)
        width, height = A4

        def add_footer(page_num):
            pdf.setFont("Helvetica", 10)
            pdf.setFillColor(colors.grey)
            pdf.drawString(100, 20, f"Page {page_num}")

        page_num = 1

        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(100, height - 60,
                       f"Profil de {profile.name} {profile.surname}")

        pdf.setLineWidth(1)
        pdf.setStrokeColor(colors.black)
        pdf.line(100, height - 80, width - 100, height - 80)  # Horizontal line

        pdf.setFont("Helvetica", 12)

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
            # Check if the file is an image and display it
            file_path = profile_file.file.path
            if os.path.exists(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                add_footer(page_num)
                pdf.showPage()  # New page for each file
                page_num += 1

                pdf.setFont("Helvetica-Bold", 14)
                pdf.drawString(100, height - 100,
                               f"Fichier: {profile_file.file.name}")
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
                    pdf.drawString(100, height - 130,
                                   f"Unable to load image: {e}")
            else:
                # pdf.drawString(100, height - 130, "Non-image file (not displayed)")
                pass

        add_footer(page_num)
        pdf.save()
        return response
    except Exception as e:
        logger.error(
            f"Error exporting profile by id: {profile_id} {e}", request=request)


@login_required
def export_profiles_csv(request):
    logger.info("Exporting profiles in csv", request=request)

    try:
        search_value = request.GET.get('search', '')
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
            profiles = profiles.filter(state__in=states)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="profiles.csv"'

        writer = csv.writer(response)

        writer.writerow([
            'Nom', 'Prénom', 'Email', 'Numéro', 'Ville', 'Compétences', 'Diplômes',
            'Date de création', 'Date de mise à jour', 'État', 'Commentaires'
        ])

        for profile in profiles:
            skills = ', '.join([skill.name for skill in profile.skills.all()])

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
    except Exception as e:
        logger.error(f"Exporting profiles in csv {e}", request=request)


@login_required
@permission_required('profiles.add_profile')
@require_http_methods(["GET"])
def check_profile(request):
    logger.debug(f"Checking profile similarity {request.GET}", request=request)
    result = {}
    try:
        data = request.GET
        name = data.get('name')
        surname = data.get('surname')
        email = data.get('email')
        number = data.get('number')

        if Profile.objects.filter(name=name).exists():
            # result['name'] = True
            pass
        if Profile.objects.filter(surname=surname).exists():
            # result['surname'] = True
            pass
        if email:
            if Profile.objects.filter(email=email).exists():
                result['email'] = True
        if Profile.objects.filter(number=number).exists():
            result['number'] = True
    except Exception as e:
        logger.error(f"Error cheking similarity {e}", request=request)

    return JsonResponse(result)


@permission_required('profiles.view_profile')
@login_required
def profiles_data(request):
    response = {
        'recordsTotal': 0,
        'recordsFiltered': 0,
        'profiles': [],
    }
    try:
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        page = int(request.GET.get('page', 1))
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

        response['recordsTotal'] = Profile.objects.count()
        response['recordsFiltered'] = paginator.count
        response['profiles'] = serializer.data
    except Exception as e:
        logger.error(f"Error fetching profiles data {e}", request=request)

    return JsonResponse(response, encoder=DjangoJSONEncoder)
