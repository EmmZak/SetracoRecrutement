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
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

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
        page_width, page_height = A4
        margins = {"top": 50, "bottom": 75, "left": 75, "right": 75}
        usable_width = page_width - margins["left"] - margins["right"]
        usable_height = page_height - margins["top"] - margins["bottom"]

        def add_section(title, content, y_position, title_font_size=16, content_font_size=12, bold=False):
            pdf.setFont("Helvetica-Bold" if bold else "Helvetica", title_font_size)
            pdf.drawString(margins["left"], y_position, title)

            pdf.setFont("Helvetica", content_font_size)
            y_position -= 20
            for item in content:
                pdf.drawString(margins["left"] + 20, y_position, str(item))
                y_position -= 20
            return y_position

        def add_paragraphs(paragraphs, y_position, x_position, width, height, font_size = 12):
            style = ParagraphStyle(name='paragraphImplicitDefaultStyle', fontSize=font_size)
            for text in paragraphs:
                paragraph = Paragraph(text, style=style)
                w, h = paragraph.wrap(width, height)
                if y_position - h < margins["bottom"]:
                    pdf.showPage()
                    y_position = page_height - margins["top"]
                paragraph.drawOn(pdf, x_position, y_position - h)
                y_position -= h + 5
            y_position -= 20
            return y_position

        # Header
        pdf.setFont("Helvetica-Bold", 22)
        pdf.drawString(margins["left"], page_height - 60,
                       f"Profil de {profile.name} {profile.surname}")
        pdf.line(margins["left"], page_height - 80,
                 page_width - margins["right"], page_height - 80)

        # Sections
        y_position = page_height - 120
        personal_info = [
            ("Email", profile.email),
            ("Numéro", profile.number),
            ("Ville", profile.town),
            ("Date de naissance", profile.birthday),
            ("Diplômes", profile.diplomas),
            ("Date de création", profile.creation_date.strftime('%d/%m/%Y %H:%M:%S')),
            ("Date de mise à jour", profile.update_date.strftime('%d/%m/%Y %H:%M:%S')),
            ("État candidature", getattr(profile.state, 'name', "Inconnu"))
        ]
        y_position = add_section("Informations Personnelles", [
                                 f"{label}: {value}" for label, value in personal_info], y_position, bold=True)

        y_position = add_section("Compétences", [
                                 skill.name for skill in profile.skills.all()], y_position, bold=True)
        y_position = add_section("Formations", [
                                 training.name for training in profile.trainings.all()], y_position, bold=True)

        y_position = add_section("Commentaires", [], y_position, bold=True)
        
        comments = [
            f"{comment.user.username}: {comment.text}" for comment in profile.comments.all()]
        y_position = add_paragraphs(
            comments, y_position, margins["left"] + 20, usable_width, usable_height)

        y_position = add_section("Suivi", [], y_position, bold=True)

        followups = [
            f"{flw.user.username}: {flw.text}" for flw in profile.followups.all()]
        y_position = add_paragraphs(
            followups, y_position, margins["left"] + 20, usable_width, usable_height)

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
            states = state_filter.split(',')
            profiles = profiles.filter(state__in=states)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="profiles.csv"'

        writer = csv.writer(response)

        writer.writerow([
            'Date de creation', 'Date de mise a jour', 'Nom', 'Prenom', 'Date de naissance',
            'Email', 'Numero', 'Ville', 'Competences', 'Diplomes',
            'Etat', 'Commentaires', 'Suivi interne', 'Formations'
        ])

        for profile in profiles:
            skills = ', '.join([skill.name for skill in profile.skills.all()])

            comments = '; '.join(
                [f"{comment.user.username}: {comment.text}" for comment in profile.comments.all()])

            followups = '; '.join(
                [f"{flw.user.username}: {flw.text}" for flw in profile.followups.all()])

            trainings = '; '.join(
                [f"{training.name}" for training in profile.trainings.all()])

            state = getattr(profile.state, 'name', "Inconnu")
            creation_date = profile.creation_date.strftime('%d/%m/%Y %H:%M:%S')
            update_date = profile.update_date.strftime('%d/%m/%Y %H:%M:%S')

            writer.writerow([
                creation_date, update_date, profile.name, profile.surname, profile.birthday,
                profile.email, profile.number, profile.town, skills, profile.diplomas,
                state, comments, followups, trainings
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
        fields = {
            "surname": data.get("surname", "").strip().lower(),
            "email": data.get("email", "").strip().lower(),
            "number": data.get("number", "").strip(),
        }

        logger.info(f"Checking fields: {fields}")

        for field, value in fields.items():
            if value and Profile.objects.filter(**{f"{field}__iexact": value}).exists():
                result[field] = True
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

        # Handle 'All' case
        if length == -1:
            serializer = ProfileSerializer(profiles, many=True)
            response['recordsFiltered'] = profiles.count()
        else:
            paginator = Paginator(profiles, length)
            profiles_page = paginator.get_page(start // length + 1)
            serializer = ProfileSerializer(profiles_page, many=True)
            response['recordsFiltered'] = paginator.count

        response['recordsTotal'] = Profile.objects.count()
        response['profiles'] = serializer.data
    except Exception as e:
        logger.error(f"Error fetching profiles data {e}", request=request)

    return JsonResponse(response, encoder=DjangoJSONEncoder)
