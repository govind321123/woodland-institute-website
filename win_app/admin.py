from django.contrib import admin
from .models import (
    OrganizationModel,
    CourseType,
    CoursesModel,
    FacilitiesModel,
    SliderModel,
    AboutUsModel,
    Designation,
    Department,
    Administration,
    Event,
    GalleryCategory,
    GalleryItem,
    Application,
    Breadcrumb,
    WhyChooseUs,
    DirectorMessage,
    ContactPage,
    Announcement,
    AnnouncementCategory,
    LeadershipMessage,
    FooterSection,
    FooterLink, 
    SitePage,
    ContactMessage,
    # FooterSection, FooterLink, SitePage
    CourseSyllabus,
    AdmissionSettings,
    Laboratory,
    



)

# ==================================================
# APPLICATION ADMIN (FIXED)
# ==================================================
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'first_name',
        'last_name',
        'email',
        'contact_number',
        'program',
        'created_at',
    )

    readonly_fields = ('created_at',)

    list_filter = ('program', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'contact_number')
    ordering = ('-created_at',)


# ==================================================
# SIMPLE REGISTRATIONS
# ==================================================
admin.site.register(OrganizationModel)
admin.site.register(CourseType)
admin.site.register(CoursesModel)
admin.site.register(FacilitiesModel)
admin.site.register(SliderModel)
admin.site.register(AboutUsModel)
admin.site.register(Designation)
admin.site.register(Department)
admin.site.register(Administration)
admin.site.register(Event)
admin.site.register(GalleryCategory)
admin.site.register(GalleryItem)
admin.site.register(Breadcrumb)
admin.site.register(WhyChooseUs)
# 

admin.site.register(Laboratory)
# admin.site.register(DirectorMessage)
@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')

# @admin.register(Announcement)
# class AnnouncementAdmin(admin.ModelAdmin):
#     list_display = ('title', 'is_active', 'created_at')
#     list_filter = ('is_active',)

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')

# announcement category
@admin.register(AnnouncementCategory)
class AnnouncementCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(LeadershipMessage)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'created_at')
    prepopulated_fields = {"slug": ("name",)}

# Footer section
class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1


@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    inlines = [FooterLinkInline]


@admin.register(SitePage)
class SitePageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(DirectorMessage)
class DirectorMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'designation')

admin.site.register(CourseSyllabus)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "subject",
        "is_read",
        "created_at",
    )

    list_filter = ("is_read", "created_at")

    search_fields = ("name", "email", "subject")

    list_editable = ("is_read",)

    readonly_fields = ("name", "email", "subject", "message", "created_at")

admin.site.register(AdmissionSettings)
