from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib import messages
from datetime import datetime
from django.utils.safestring import mark_safe
from .models import SitePage
from .util import sent_email
from .forms import ApplicationForm
from django.urls import reverse_lazy
from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import redirect



# changes
# from .models import Announcement





from .models import (
    OrganizationModel,
    DirectorMessage,
    CoursesModel,
    FacilitiesModel,
    GalleryCategory,
    Administration,
    Event,
    Application,
    Breadcrumb,
    WhyChooseUs,
    ContactPage,
    Announcement,
    AnnouncementCategory,
    LeadershipMessage,
    SitePage,
    CoursesModel,
    ContactMessage,

)



class IndexView(View):
    def get(self, request):
        organization = OrganizationModel.objects.first()
        director = DirectorMessage.objects.filter(is_active=True).first()

        # FIXED ORDER
        courses = CoursesModel.objects.order_by('heads')

        leaders = LeadershipMessage.objects.all()

        current_year = datetime.now().year
        year_of_establishment = None

        if organization and organization.year_of_estabishment:
            year_of_establishment = current_year - organization.year_of_estabishment

        return render(request, "index.html", {
            "organization": organization,
            "yearofestablishment": year_of_establishment,
            "director": director,
            "courses": courses,
            "leaders": leaders,
        })

# class IndexView(View):
#     def get(self, request):
#         organization = OrganizationModel.objects.first()
#         director = DirectorMessage.objects.filter(is_active=True).first()
#         # courses = CoursesModel.objects.all()[:3]
#         courses = CoursesModel.objects.all()

#         leaders = LeadershipMessage.objects.all()  # 👈 ADD THIS

#         current_year = datetime.now().year
#         year_of_establishment = None

#         if organization and organization.year_of_estabishment:
#             year_of_establishment = current_year - organization.year_of_estabishment

#         return render(request, "index.html", {
#             "organization": organization,
#             "yearofestablishment": year_of_establishment,
#             "director": director,
#             "courses": courses,
#             "leaders": leaders,   # 👈 ADD THIS
#         })






# ==================================================
# COURSES (DETAIL PAGE)
# ==================================================




class CoursesView(View):
    def get(self, request, slug):
        course = get_object_or_404(CoursesModel, slug=slug)

        breadcrumb_image = (
            course.breadcrumb_image.url
            if course.breadcrumb_image
            else None
        )

        if not breadcrumb_image:
            section_bc = Breadcrumb.objects.filter(section="courses").first()
            if section_bc and section_bc.image:
                breadcrumb_image = section_bc.image.url

        # 🔥 SPLIT CONTENT AFTER FIRST PARAGRAPH
        content = course.details or ""
        parts = content.split("</p>", 1)

        first_part = ""
        second_part = ""

        if len(parts) > 1:
            first_part = parts[0] + "</p>"
            second_part = parts[1]
        else:
            first_part = content

        return render(request, "courses.html", {
            "singlecourse": course,
            "breadcrumb_image": breadcrumb_image,
            "section_heading": course.heads,
            "first_part": first_part,
            "second_part": second_part,
        })




# ==================================================
# FACILITIES
# ==================================================
class FacilitiesView(View):
    def get(self, request, slug):
        facility = get_object_or_404(FacilitiesModel, slug=slug)

        breadcrumb_image = (
            facility.breadcrumb_image.url
            if facility.breadcrumb_image
            else None
        )

        if not breadcrumb_image:
            section_bc = Breadcrumb.objects.filter(section="facilities").first()
            if section_bc and section_bc.image:
                breadcrumb_image = section_bc.image.url

        return render(request, "facilities.html", {
            "singlefacilities": facility,
            "breadcrumb_image": breadcrumb_image,
            "section_heading": facility.heads,
        })


# ==================================================
# GALLERY
# ==================================================
class GalleryView(View):
    def get(self, request, slug):
        category = get_object_or_404(GalleryCategory, slug=slug)
        items = category.items.all()
        categories = GalleryCategory.objects.all()

        breadcrumb_image = (
            category.breadcrumb_image.url
            if category.breadcrumb_image
            else None
        )

        if not breadcrumb_image:
            section_bc = Breadcrumb.objects.filter(section="gallery").first()
            if section_bc and section_bc.image:
                breadcrumb_image = section_bc.image.url

        return render(request, "gallery.html", {
            "category": category,
            "gallery_items": items,
            "gallery_categories": categories,
            "breadcrumb_image": breadcrumb_image,
            "section_heading": category.name,
        })


# ==================================================
# CONTACT
# ==================================================
class ContactView(View):
    def get(self, request):
        organization = OrganizationModel.objects.first() 
        contact_page = ContactPage.objects.filter(is_active=True).first()

        breadcrumb_image = None

        # 1️⃣ Try breadcrumb table first
        section_bc = Breadcrumb.objects.filter(section="contact").first()
        if section_bc and section_bc.image:
            breadcrumb_image = section_bc.image.url

        # 2️⃣ Fallback to contact page image
        elif contact_page and contact_page.image:
            breadcrumb_image = contact_page.image.url

        return render(request, "contact.html", {
            "breadcrumb_image": breadcrumb_image,
            "section_heading": "Contact Us",
            "contact_page": contact_page,
            "organization": organization, 
        })




    
class SendEmailView(View):

    def post(self, request):

        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # ✅ Save message to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # ✅ Send email (your existing function)
        sent_email(request, name, email, subject, message)

        messages.success(request, "Email sent successfully")

        return redirect("contact")



    
class AdministrationListView(ListView):
    model = Administration
    template_name = 'administration.html'
    context_object_name = 'administrations'

    def get_queryset(self):
        return Administration.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ===============================
        # 1️⃣ PRINCIPAL & VICE PRINCIPAL ORDER
        # ===============================
        context["principal_staff"] = (
            Administration.objects.filter(
                is_active=True,
                designation__name__in=["Principal", "Vice Principal"]
            )
            .annotate(
                custom_order=Case(
                    When(designation__name="Principal", then=Value(1)),
                    When(designation__name="Vice Principal", then=Value(2)),
                    output_field=IntegerField(),
                )
            )
            .order_by("custom_order")
        )

        # ===============================
        # 2️⃣ BSC / PBSC ORDER
        # ===============================
        context["bsc_staff"] = (
            Administration.objects.filter(
                is_active=True,
                faculty_category="bsc"
            )
            .annotate(
                custom_order=Case(
                    When(designation__name="Associate Professor", then=Value(1)),
                    When(designation__name="Assistant Professor", then=Value(2)),
                    When(designation__name="Lecturer", then=Value(3)),
                    When(designation__name="Tutor", then=Value(4)),
                    default=Value(5),
                    output_field=IntegerField(),
                )
            )
            .order_by("custom_order")
        )

        # ===============================
        # 3️⃣ GNM ORDER (Same Pattern)
        # ===============================
        context["gnm_staff"] = (
            Administration.objects.filter(
                is_active=True,
                faculty_category="gnm"
            )
            .annotate(
                custom_order=Case(
                    When(designation__name="Associate Professor", then=Value(1)),
                    When(designation__name="Assistant Professor", then=Value(2)),
                    When(designation__name="Lecturer", then=Value(3)),
                    When(designation__name="Tutor", then=Value(4)),
                    default=Value(5),
                    output_field=IntegerField(),
                )
            )
            .order_by("custom_order")
        )

        # Breadcrumb
        section_bc = Breadcrumb.objects.filter(section="administration").first()
        
        breadcrumb_image = section_bc.image.url if section_bc and section_bc.image else None

        context.update({
            "breadcrumb_image": breadcrumb_image,
            "section_heading": "Administration",
        })

        return context



class AdministrationDetailView(DetailView):
    model = Administration
    template_name = "win_app/administration_detail.html"
    context_object_name = "administration"

  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        section_bc = Breadcrumb.objects.filter(section="administration").first()

        breadcrumb_image = section_bc.image.url if section_bc and section_bc.image else None

        context["breadcrumb_image"] = breadcrumb_image
        context["section_heading"] = "Administration"
        context["page_title"] = self.object.name

        return context


# ==================================================
# EVENTS
# ==================================================
class EventListView(View):
    def get(self, request):
        events = Event.objects.all()

        section_bc = Breadcrumb.objects.filter(section="events").first()
        breadcrumb_image = section_bc.image.url if section_bc and section_bc.image else None

        return render(request, "win_app/event_list.html", {
            "events": events,
            "breadcrumb_image": breadcrumb_image,
            "section_heading": "Events",
        })


class EventDetailView(View):
    def get(self, request, slug):
        event = get_object_or_404(Event, slug=slug)

        section_bc = Breadcrumb.objects.filter(section="events").first()
        breadcrumb_image = section_bc.image.url if section_bc and section_bc.image else None

        return render(request, "win_app/event_detail.html", {
            "event": event,
            "breadcrumb_image": breadcrumb_image,
            "section_heading": event.title,
        })


# ==================================================
# APPLY NOW
# ==================================================
class ApplyNowView(FormView):
    template_name = "apply_now.html"
    form_class = ApplicationForm
    success_url = reverse_lazy('application_success')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Application submitted successfully")
        return super().form_valid(form)

class ApplicationSuccessView(View):
    def get(self, request):
        return render(request, "application_success.html", {
            "section_heading": "Application Submitted",
        })


# ==================================================
# TRAINING
# ==================================================
class TrainingView(View):
    def get(self, request):
        section_bc = Breadcrumb.objects.filter(section="training").first()
        breadcrumb_image = section_bc.image.url if section_bc and section_bc.image else None

        return render(request, "win_app/training.html", {
            "breadcrumb_image": breadcrumb_image,
            "section_heading": "Training",
            "hide_home_sections": True,   # 👈 IMPORTANT
        })


# ==================================================
# WHY CHOOSE US
# ==================================================
class WhyChooseUsView(View):
    def get(self, request):
        why = WhyChooseUs.objects.filter(is_active=True).first()

        breadcrumb_image = None
        if why and why.breadcrumb_image:
            breadcrumb_image = why.breadcrumb_image.url

        return render(
            request,
            "win_app/why_choose_us.html",
            {
                "why": why,
                "breadcrumb_image": breadcrumb_image,
                "section_heading": "Why Choose Woodland Nursing Institute",
            }
        )
# Administration
# ==================================================
class AnnouncementListView(ListView):
    model = Announcement
    template_name = "announcements/announcement_list.html"
    context_object_name = "announcements"

    def get_queryset(self):
        # Get active category by slug
        self.category = get_object_or_404(
            AnnouncementCategory,
            slug=self.kwargs["slug"],
            is_active=True
        )

        return Announcement.objects.filter(
            is_active=True,
            category=self.category
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["category"] = self.category

        # Breadcrumb
        section_bc = Breadcrumb.objects.filter(section="announcements").first()
        context["breadcrumb_image"] = (
            section_bc.image.url if section_bc and section_bc.image else None
        )

        # 🔥 SAFE FIELD DETECTION (NO MORE ERRORS)
        if hasattr(self.category, "heads"):
            context["section_heading"] = self.category.heads
        elif hasattr(self.category, "title"):
            context["section_heading"] = self.category.title
        elif hasattr(self.category, "name"):
            context["section_heading"] = self.category.name
        else:
            context["section_heading"] = "Announcements"

        return context
# class AnnouncementListView(ListView):
#     model = Announcement
#     template_name = "announcements/announcement_list.html"
#     context_object_name = "announcements"

#     def get_queryset(self):
#         self.category = get_object_or_404(
#             AnnouncementCategory,
#             slug=self.kwargs["slug"],
#             is_active=True
#         )

#         return Announcement.objects.filter(
#             is_active=True,
#             category=self.category
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         # 🔥 ADD CATEGORY TO CONTEXT
#         context["category"] = self.category

#         bc = Breadcrumb.objects.filter(section="announcements").first()
#         context["breadcrumb_image"] = bc.image.url if bc and bc.image else None

#         return context


# class AnnouncementDetailView(DetailView):
#     model = Announcement
#     template_name = "announcements/announcement_detail.html"
#     context_object_name = "announcement"
#     slug_field = "slug"
#     slug_url_kwarg = "slug"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         section_bc = Breadcrumb.objects.filter(section="announcements").first()
#         context["breadcrumb_image"] = (
#             section_bc.image.url if section_bc and section_bc.image else None
#         )
#         context["section_heading"] = self.object.title

#         return context
    


class LeadershipListView(ListView):
    model = LeadershipMessage
    template_name = 'leadership.html'
    context_object_name = 'leadership_messages'
    ordering = ['-created_at']

class LeadershipDetailView(DetailView):
    model = LeadershipMessage
    template_name = 'leadership_detail.html'
    context_object_name = 'leader'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_home_sections'] = True
        return context


# class LeadershipDetailView(DetailView):
#     model = LeadershipMessage
#     template_name = 'leadership_detail.html'
#     context_object_name = 'leader'




class DynamicPageView(DetailView):
    model = SitePage
    template_name = "dynamic_page.html"
    context_object_name = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_home_sections'] = True   # 🔥 THIS IS THE MAGIC
        return context
    




# ==================================================
# DASHBOARD
# ==================================================

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class DashboardHomeView(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = '/secretadmin/login/'

    def test_func(self):
        # Only staff users allowed
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('home')

    def get(self, request):

        total_applications = Application.objects.count()
        recent_applications = Application.objects.all().order_by('-id')[:10]

        return render(
            request,
            "dashboard/home.html",
            {
                "total_applications": total_applications,
                "recent_applications": recent_applications,
            }
        )


# ==================================================
# COURSE SYLLABUS (CLASS BASED VIEW)
# ==================================================

class CourseSyllabusView(View):
    def get(self, request, slug):
        course = get_object_or_404(CoursesModel, slug=slug)
        syllabus = getattr(course, "syllabus", None)

        breadcrumb_image = None

        # 1️⃣ Try course specific breadcrumb
        if hasattr(course, "breadcrumb_image") and course.breadcrumb_image:
            breadcrumb_image = course.breadcrumb_image.url

        # 2️⃣ Fallback to Courses section breadcrumb
        if not breadcrumb_image:
            section_bc = Breadcrumb.objects.filter(section="courses").first()
            if section_bc and section_bc.image:
                breadcrumb_image = section_bc.image.url

        return render(
            request,
            "course_syllabus.html",
            {
                "course": course,
                "syllabus": syllabus,
                "breadcrumb_image": breadcrumb_image,
                "section_heading": f"{course.heads} - Program Structure",
            }
        )