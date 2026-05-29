from django.db.models import Case, When, Value, IntegerField
from django.utils import timezone

from .models import (
    OrganizationModel,
    CoursesModel,
    FacilitiesModel,
    SliderModel,
    AboutUsModel,
    Administration,
    Event,
    GalleryCategory,
    AnnouncementCategory,
    LeadershipMessage,
    FooterSection,
    AdmissionSettings,   # 👈 ADD THIS
)


# ==============================
# ✅ MENU DATA
# ==============================
def menus(request):
    return {
        "organization": OrganizationModel.objects.first(),
        "courses": CoursesModel.objects.all(),
        "facilities": FacilitiesModel.objects.all(),
        "slider": SliderModel.objects.all(),
        "events": Event.objects.all(),
        "aboutus": AboutUsModel.objects.all().values("excerpt").first(),
        "administrations": Administration.objects.filter(is_active=True),
        "galleries": GalleryCategory.objects.all(),
        "announcement_categories": AnnouncementCategory.objects.filter(is_active=True),
        "leadership_messages": LeadershipMessage.objects.all(),
    }


# ==============================
# ✅ FOOTER
# ==============================
def footer_sections(request):

    sections = FooterSection.objects.prefetch_related("links").annotate(
        custom_order=Case(
            When(name="Institute Policies", then=Value(1)),
            When(name="Our Campus", then=Value(2)),
            When(name="Quick Links", then=Value(3)),
            default=Value(4),
            output_field=IntegerField(),
        )
    ).order_by("custom_order")

    return {
        "footer_sections": sections
    }


# ==============================
# ✅ ADMISSION STATUS
# ==============================
def admission_status(request):

    setting = AdmissionSettings.objects.filter(is_active=True).first()

    if not setting:
        return {"admission_open": False}

    today = timezone.now().date()

    return {
        "admission_open": setting.start_date <= today <= setting.end_date
    }



# from django.db.models import Case, When, Value, IntegerField

# from .models import (
#     OrganizationModel,
#     CoursesModel,
#     FacilitiesModel,
#     SliderModel,
#     AboutUsModel,
#     Administration,
#     Event,
#     GalleryCategory,
#     AnnouncementCategory,
#     LeadershipMessage,
#     FooterSection
# )


# def menus(request):
#     return {
#         "organization": OrganizationModel.objects.first(),
#         "courses": CoursesModel.objects.all(),
#         "facilities": FacilitiesModel.objects.all(),
#         "slider": SliderModel.objects.all(),
#         "events": Event.objects.all(),
#         "aboutus": AboutUsModel.objects.all().values("excerpt").first(),
#         "administrations": Administration.objects.filter(is_active=True),
#         "galleries": GalleryCategory.objects.all(),
#         "announcement_categories": AnnouncementCategory.objects.filter(is_active=True),
#         "leadership_messages": LeadershipMessage.objects.all(),
#     }


# def footer_sections(request):

#     sections = FooterSection.objects.prefetch_related("links").annotate(
#         custom_order=Case(
#             When(name="Institute Policies", then=Value(1)),
#             When(name="Our Campus", then=Value(2)),
#             When(name="Quick Links", then=Value(3)),
#             default=Value(4),
#             output_field=IntegerField(),
#         )
#     ).order_by("custom_order")

#     return {
#         "footer_sections": sections
#     }

    










