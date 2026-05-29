from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import (
    IndexView,
    CoursesView,
    CourseSyllabusView,   # ✅ Added
    FacilitiesView,
    GalleryView,
    ContactView,
    SendEmailView,
    EventListView,
    EventDetailView,
    ApplyNowView,
    TrainingView,
    WhyChooseUsView,
    AdministrationListView,
    AdministrationDetailView,
    ApplicationSuccessView,
    AnnouncementListView,
    LeadershipListView,
    LeadershipDetailView,
    DynamicPageView,
    DashboardHomeView,
    DownloadApplicationView,
    DownloadApplicationByIDView, 
    ApplicationListView,
    LaboratoryListView,
     
)

urlpatterns = [

    # =========================
    # HOME
    # =========================
    path('', IndexView.as_view(), name='home'),

    # =========================
    # DASHBOARD (STAFF ONLY)
    # =========================
    path('dashboard/', DashboardHomeView.as_view(), name='dashboard_home'),

    # =========================
    # COURSES
    # =========================
    path('courses/<slug:slug>/', CoursesView.as_view(), name='courses'),

    # =========================
    # COURSE SYLLABUS
    # =========================
    path(
        'courses/<slug:slug>/syllabus/',
        CourseSyllabusView.as_view(),
        name='course_syllabus'
    ),

    # =========================
    # FACILITIES
    # =========================
    path('facilities/<slug:slug>/', FacilitiesView.as_view(), name='facilities'),

    # =========================
    # GALLERY
    # =========================
    # path('gallery/<slug:slug>/', GalleryView.as_view(), name='gallery'),

    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('gallery/<slug:slug>/', GalleryView.as_view(), name='gallery_category'),

    # =========================
    # CONTACT
    # =========================
    path('contact/', ContactView.as_view(), name='contact'),
    path('email/', SendEmailView.as_view(), name='email'),

    # =========================
    # EVENTS
    # =========================
    path('events/', EventListView.as_view(), name='events'),
    path('events/<slug:slug>/', EventDetailView.as_view(), name='event_detail'),

    # =========================
    # ADMISSION / APPLICATION
    # =========================
    path('apply-now/', ApplyNowView.as_view(), name='apply_now'),
    path('admission/', ApplyNowView.as_view(), name='admission'),
    # path('success/', ApplicationSuccessView.as_view(), name='application_success'),
    path(
    "application-success/<int:id>/",
    ApplicationSuccessView.as_view(),
    name="application_success"
    ),

    path(
        "download-application/<int:id>/",
        DownloadApplicationView.as_view(),
        name="download_application"
    ),

    path(
    "download-application/",
    DownloadApplicationByIDView.as_view(),
    name="download_application_by_id"
),

    # =========================
    # ADMINISTRATION
    # =========================
    path('administration/', AdministrationListView.as_view(), name='administration'),
    path(
        'administration/<slug:slug>/',
        AdministrationDetailView.as_view(),
        name='administration_detail'
    ),

    # =========================
    # TRAINING / WHY CHOOSE US
    # =========================
    path('training/', TrainingView.as_view(), name='training'),
    path('why-choose-us/', WhyChooseUsView.as_view(), name='why_choose_us'),

    # =========================
    # ANNOUNCEMENTS
    # =========================
    path(
        'announcements/',
        AnnouncementListView.as_view(),
        name='announcements_home'
    ),
    path(
        'announcements/<slug:slug>/',
        AnnouncementListView.as_view(),
        name='announcement_category'
    ),

    # =========================
    # LEADERSHIP
    # =========================
    path('leadership/', LeadershipListView.as_view(), name='leadership_list'),
    path(
        'leadership/<slug:slug>/',
        LeadershipDetailView.as_view(),
        name='leadership_detail'
    ),


    # =========================
    # CUSTOM DATA VIEW
    # =========================
    path('applications/', ApplicationListView.as_view(), name='applications'),


    path('facilities/laboratories/', LaboratoryListView.as_view(), name='laboratories'),


    # ======================================================
    # 🚨 IMPORTANT: KEEP THIS ALWAYS LAST
    # CATCH-ALL DYNAMIC PAGE
    # ======================================================
    path('<slug:slug>/', DynamicPageView.as_view(), name='dynamic_page'),


]


# =========================
# MEDIA FILES (DEV ONLY)
# =========================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)