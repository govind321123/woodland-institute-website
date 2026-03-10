from .models import (
    OrganizationModel, CoursesModel, FacilitiesModel, SliderModel,
    AboutUsModel, Administration, Event, GalleryCategory,AnnouncementCategory, LeadershipMessage, FooterSection # 👈 ADD THIS FooterSection
   

)


def menus(request):
    return {
        "organization": OrganizationModel.objects.first(),
        "courses": CoursesModel.objects.all(),
        "facilities": FacilitiesModel.objects.all(),
        "slider": SliderModel.objects.all(),
        "events": Event.objects.all(),
        "aboutus": AboutUsModel.objects.all().values("excerpt").first(),
        "administrations": Administration.objects.all(),
        "galleries": GalleryCategory.objects.all(),   # <-- FIXED NAME
        'administrations': Administration.objects.filter(is_active=True),
        "announcement_categories": AnnouncementCategory.objects.filter(is_active=True),
        # 👇 ADD THIS
        "leadership_messages": LeadershipMessage.objects.all(),
        
    }

def footer_sections(request):
    sections = FooterSection.objects.prefetch_related('links').all()
    return {'footer_sections': sections}

    
# def admission_menu(request):
#     return {
#         'admissions': Admission.objects.filter(is_active=True)
#     }









# from .models import (
#     OrganizationModel, CoursesModel, FacilitiesModel, SliderModel,
#     GalleryCategory, GalleryItem, AboutUsModel, Administration, Event
# )

# def menus(request):
#     organization = OrganizationModel.objects.first()
#     courses = CoursesModel.objects.all()
#     events = Event.objects.all()
#     facilities = FacilitiesModel.objects.all()
#     slider = SliderModel.objects.all()

#     # New gallery data
#     gallery_categories = GalleryCategory.objects.all()
#     gallery_items = GalleryItem.objects.all()

#     aboutus = AboutUsModel.objects.all().values('excerpt').first()
#     administrations = Administration.objects.all()
   
#     return dict(
#         organization=organization,
#         courses=courses,
#         facilities=facilities,
#         slider=slider,

#         # updated gallery references
#         gallery_categories=gallery_categories,
#         gallery_items=gallery_items,

#         aboutus=aboutus,
#         administrations=administrations,
#         events=events,
#     )










# from .models import OrganizationModel, CoursesModel, FacilitiesModel, SliderModel, GalleryModel, AboutUsModel,  Administration, Event  # ← ADD THIS
# def menus(request):
#     organization = OrganizationModel.objects.first()
#     courses = CoursesModel.objects.all()
#     events = Event.objects.all ()
#     facilities = FacilitiesModel.objects.all()
#     slider = SliderModel.objects.all()
#     gallery = GalleryModel.objects.all()
#     aboutus = AboutUsModel.objects.all().values('excerpt').first(),
#     administrations = Administration.objects.all()  # ← ADD THIS
   
     
#     return dict(
#         organization=organization,
#         courses=courses,
#         facilities=facilities,
#         slider=slider,
#         gallery=gallery,
#         aboutus=aboutus,
#          administrations=administrations,  # ← ADD THIS
#          events = events,
#         )