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

from .models import Comment, Profile, ProfileFile, FollowUp

logger = Logger('profiles')


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
            return HttpResponse(status=200)
    except Exception as e:
        logger.error(
            f"Error deleting comment by id: {com_id} {e}", request=request)
        return HttpResponse(status=500)

    return HttpResponse(status=400)


@login_required
@permission_required('profiles.delete_followup')
@require_http_methods(["DELETE"])
def delete_followup(request):
    flw_id = request.GET.get('id')
    logger.info(f"Deleting followup by id: {flw_id}", request=request)
    try:
        if flw_id:
            FollowUp.objects.filter(id=flw_id).delete()
            print("returning success")
            return HttpResponse(status=200)
    except Exception as e:
        logger.error(
            f"Error deleting followup by id: {flw_id} {e}", request=request)
        return HttpResponse(status=500)

    return HttpResponse(status=400)


@login_required
@permission_required('profiles.delete_profilefile')
@require_http_methods(["DELETE"])
def delete_file(request):
    file_id = request.GET.get('id')
    logger.info(f"Deleting file by id: {file_id}", request=request)
    try:
        if file_id:
            ProfileFile.objects.filter(id=file_id).delete()
            return HttpResponse(status=200)
    except Exception as e:
        logger.error(
            f"Error deleting file by id: {file_id} {e}", request=request)
        return HttpResponse(status=500)

    return HttpResponse(status=400)


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

        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(100, height - 60,
                       f"Profil de {profile.name} {profile.surname}")

        pdf.setLineWidth(1)
        pdf.setStrokeColor(colors.black)
        pdf.line(100, height - 80, width - 100, height - 80)  # Horizontal line

        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(100, height - 120, "Informations Personnelles")
        pdf.setFont("Helvetica", 12)
        y_position = height - 140

        profile_details = [
            ("Email", profile.email),
            ("Numéro", profile.number),
            ("Ville", profile.town),
            # ("Compétences", ', '.join([skill.name for skill in profile.skills.all()])),
            ("Date de naissance", profile.birthday),
            ("Diplômes", profile.diplomas),
            ("Date de création", profile.creation_date.strftime('%d/%m/%Y %H:%M:%S')),
            ("Date de mise à jour", profile.update_date.strftime('%d/%m/%Y %H:%M:%S')),
            ("Etat candidature", getattr(profile.state, 'name', "Inconnu"))
        ]

        for label, value in profile_details:
            pdf.drawString(120, y_position, f"{label}: {value}")
            y_position -= 20

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100, y_position, "Compétences:")
        y_position -= 20
        pdf.setFont("Helvetica", 12)

        for skill in profile.skills.all():
            pdf.drawString(120, y_position, skill.name)
            y_position -= 20

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(100, y_position, "Formations:")
        y_position -= 20
        pdf.setFont("Helvetica", 12)

        for training in profile.trainings.all():
            pdf.drawString(120, y_position, training.name)
            y_position -= 20

        add_footer(page_num)
        pdf.save()
        return response
    except Exception as e:
        logger.error(
            f"Error exporting profile by id: {profile_id} {e}", request=request)
        return HttpResponse(status=500)


@login_required
def export_profiles_csv(request):
    logger.info("Exporting profiles in csv", request=request)

    try:
        search_value = request.GET.get('search', '')
        skill_filter = request.GET.get('skills', '')
        state_filter = request.GET.get('states', '')
        training_filter = request.GET.get('trainings', '')

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

        if training_filter:
            training_ids = training_filter.split(',')
            profiles = profiles.filter(
                trainings__id__in=training_ids).distinct()

        if state_filter:
            states = state_filter.split(',')
            profiles = profiles.filter(state__in=states)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="profiles.csv"'

        writer = csv.writer(response)

        writer.writerow([
            'Date de creation', 'Date de mise a jour', 'Nom', 'Prenom', 'Date de naissance',
            'Email', 'Numero', 'Ville', 'Competences', 'Diplomes',
            'Etat', 'Commentaires', 'Formations'
        ])

        for profile in profiles:
            skills = ', '.join([skill.name for skill in profile.skills.all()])

            comments = '; '.join(
                [f"{comment.user.username}: {comment.text}" for comment in profile.comments.all()])

            trainings = '; '.join(
                [f"{training.name}" for training in profile.trainings.all()])

            state = getattr(profile.state, 'name', "Inconnu")
            creation_date = profile.creation_date.strftime('%d/%m/%Y %H:%M:%S')
            update_date = profile.update_date.strftime('%d/%m/%Y %H:%M:%S')

            writer.writerow([
                creation_date, update_date, profile.name, profile.surname, profile.birthday,
                profile.email, profile.number, profile.town, skills, profile.diplomas,
                state, comments, trainings
            ])

        return response
    except Exception as e:
        logger.error(f"Exporting profiles in csv {e}", request=request)
        return HttpResponse(status=500)


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
        search_value = request.GET.get('search', '')
        # comma-separated list of IDs
        skill_filter = request.GET.get('skills', '')
        training_filter = request.GET.get('trainings', '')
        state_filter = request.GET.get('states', '')
        sort_key = request.GET.get('sortBy[key]', 'creation_date')
        sort_order = request.GET.get('sortBy[order]', 'desc')

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

        if training_filter:
            training_ids = training_filter.split(',')
            profiles = profiles.filter(
                trainings__id__in=training_ids).distinct()

        if state_filter:
            state_ids = state_filter.split(',')
            profiles = profiles.filter(state__id__in=state_ids).distinct()

        if sort_key == 'state.name':
            sort_key = 'state__name'

        if sort_key:
            if sort_order == 'desc':
                # Prepend a minus sign for descending order
                sort_key = f'-{sort_key}'
            profiles = profiles.order_by(sort_key)

        paginator = Paginator(profiles, length)
        profiles_page = paginator.get_page(start // length + 1)

        serializer = ProfileSerializer(profiles_page, many=True)

        response['recordsTotal'] = Profile.objects.count()
        response['recordsFiltered'] = paginator.count
        response['profiles'] = serializer.data
    except Exception as e:
        logger.error(f"Error fetching profiles data {e}", request=request)

    return JsonResponse(response, encoder=DjangoJSONEncoder)
