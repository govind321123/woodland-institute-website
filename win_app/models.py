from django.db import models
from django.utils.text import slugify

# ==================================================
# ORGANIZATION
# ==================================================
class OrganizationModel(models.Model):
    class Meta:
        db_table = 't_organizationsetup'
        verbose_name_plural = 'ORGANIZATION SETUP'

    heads = models.CharField(max_length=100, unique=True)
    address_name = models.CharField(max_length=100)
    email_id = models.EmailField(max_length=50)
    contact_no = models.CharField(max_length=50)
    year_of_estabishment = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heads


# ==================================================
# COURSES
# ==================================================
class CourseType(models.Model):
    class Meta:
        db_table = 't_coursetype'
        verbose_name_plural = 'COURSE TYPE'

    heads = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.heads


class CoursesModel(models.Model):
    class Meta:
        db_table = 't_courses'
        verbose_name_plural = 'COURSES'

    type = models.ForeignKey(CourseType, on_delete=models.CASCADE)
    heads = models.CharField(max_length=75, unique=True)
    full_name = models.CharField(   
        max_length=150,
        blank=True,
        null=True
    )
    no_of_semester = models.CharField(max_length=50)
    total_seats = models.CharField(max_length=50)
    no_of_years = models.CharField(max_length=50)
    # course_fees = models.CharField(max_length=50)
    excerpt = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    # ✅ 1. Breadcrumb (Top Banner)
    breadcrumb_image = models.ImageField(
        upload_to='breadcrumbs/courses/',
        blank=True,
        null=True
    )

    # ✅ 2. Main Image (Inside Page)
    main_image = models.ImageField(
        upload_to='courses/main/',
        blank=True,
        null=True
    )

    # ✅ 3. Highlight Image 1
    highlight_image_1 = models.ImageField(
        upload_to='courses/highlights/',
        blank=True,
        null=True
    )

    # ✅ 4. Highlight Image 2
    highlight_image_2 = models.ImageField(
        upload_to='courses/highlights/',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.heads)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.heads

# class CoursesModel(models.Model):
#     class Meta:
#         db_table = 't_courses'
#         verbose_name_plural = 'COURSES'

#     type = models.ForeignKey(CourseType, on_delete=models.CASCADE)
#     heads = models.CharField(max_length=75, unique=True)
#     no_of_semester = models.CharField(max_length=50)
#     total_seats = models.CharField(max_length=50)
#     no_of_years = models.CharField(max_length=50)
#     course_fees = models.CharField(max_length=50)
#     excerpt = models.TextField(blank=True, null=True)
#     details = models.TextField(blank=True, null=True)
#     slug = models.SlugField(unique=True, blank=True)

#     breadcrumb_image = models.ImageField(
#         upload_to='breadcrumbs/courses/',
#         blank=True,
#         null=True
#     )

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.heads)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.heads


# ==================================================
# FACILITIES
# ==================================================
class FacilitiesModel(models.Model):
    class Meta:
        db_table = 't_facilities'
        verbose_name_plural = 'FACILITIES'

    heads = models.CharField(max_length=50, unique=True)
    excerpt = models.CharField(max_length=200, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    breadcrumb_image = models.ImageField(
        upload_to='breadcrumbs/facilities/',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.heads)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.heads


# ==================================================
# SLIDER
# ==================================================
class SliderModel(models.Model):
    class Meta:
        db_table = 't_slider'
        verbose_name_plural = 'SLIDER'

    header = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    details = models.CharField(max_length=500)
    slider_image = models.ImageField(upload_to='slider/')

    def __str__(self):
        return self.title


# ==================================================
# ABOUT US
# ==================================================
class AboutUsModel(models.Model):
    class Meta:
        db_table = 't_aboutus'
        verbose_name_plural = 'ABOUT US'

    heads = models.CharField(max_length=50, blank=True, null=True)
    excerpt = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.heads or "About Us"


# ==================================================
# ADMINISTRATION
# ==================================================
class Designation(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Administration(models.Model):

    LAYOUT_CHOICES = [
        ('landscape', 'Landscape'),
        ('portrait', 'Portrait'),
    ]

    FOCUS_CHOICES = [
        ('top', 'Face / Head'),
        ('center', 'Upper Body'),
        ('lower', 'Waist / Lower Body'),
    ]

    # ✅ ADD THIS NEW BLOCK
    FACULTY_CATEGORY = [
        ('bsc', 'BSc / PBSc'),
        ('gnm', 'GNM'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    designation = models.ForeignKey(
        Designation, on_delete=models.SET_NULL, null=True, blank=True
    )

       # ✅ NEW OPTIONAL QUALIFICATION FIELD
    qualification = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )

    # ✅ ADD THIS FIELD
    faculty_category = models.CharField(
        max_length=20,
        choices=FACULTY_CATEGORY,
        blank=True,
        null=True
    )

    details = models.TextField(blank=True)
    photo = models.ImageField(upload_to="administration/", blank=True, null=True)

    image_layout = models.CharField(
        max_length=20,
        choices=LAYOUT_CHOICES,
        default='landscape'
    )

    image_focus = models.CharField(
        max_length=20,
        choices=FOCUS_CHOICES,
        default='center'
    )

    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            i = 1
            while Administration.objects.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ==================================================
# EVENTS
# ==================================================
class Event(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField(blank=True, null=True)
    details = models.TextField(blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            base = slugify(self.title)
            slug = base
            i = 1
            while Event.objects.filter(slug=slug).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or "Event"
# class Event(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     date = models.DateField()
#     details = models.TextField()
#     image = models.ImageField(upload_to='events/')
#     slug = models.SlugField(unique=True, blank=True)

#     class Meta:
#         ordering = ['-date']

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             base = slugify(self.title)
#             slug = base
#             i = 1
#             while Event.objects.filter(slug=slug).exists():
#                 slug = f"{base}-{i}"
#                 i += 1
#             self.slug = slug
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return self.title


# ==================================================
# GALLERY
# ==================================================
class GalleryCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    breadcrumb_image = models.ImageField(
        upload_to='breadcrumbs/gallery/',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    category = models.ForeignKey(
        GalleryCategory, on_delete=models.CASCADE, related_name='items'
    )
    heads = models.CharField(max_length=50)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.heads



# ==================================================
# APPLICATION
# ==================================================
class Application(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    # ✅ NEW FIELDS
    father_first_name = models.CharField(max_length=100)
    father_last_name = models.CharField(max_length=100)

    mother_first_name = models.CharField(max_length=100)
    mother_last_name = models.CharField(max_length=100)

    dob = models.DateField()

    email = models.EmailField()
    contact_number = models.CharField(max_length=20)

    address = models.TextField()

    program = models.ForeignKey(
        CoursesModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    photo = models.ImageField(
        upload_to='applications/photos/',
        blank=True,
        null=True
    )

    document = models.FileField(
        upload_to='applications/documents/',
        blank=True,
        null=True
    )

    agree = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()
# class Application(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100, blank=True, null=True)

#     father_name = models.CharField(max_length=150)
#     mother_name = models.CharField(max_length=150)

#     dob = models.DateField()

#     email = models.EmailField()
#     contact_number = models.CharField(max_length=20)

#     address = models.TextField()

#     program = models.ForeignKey(
#         CoursesModel,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )

#     photo = models.ImageField(
#         upload_to='applications/photos/',
#         blank=True,
#         null=True
#     )

#     document = models.FileField(
#         upload_to='applications/documents/',
#         blank=True,
#         null=True
#     )

#     agree = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name or ''}".strip()


# ==================================================
# BREADCRUMB
# ==================================================
class Breadcrumb(models.Model):
    SECTION_CHOICES = [
        ('courses', 'Courses'),
        ('facilities', 'Facilities'),
        ('gallery', 'Gallery'),
        ('events', 'Events'),
        ('administration', 'Administration'),
        ('training', 'Training'),
        ('applications', 'Applications'),
        ('announcements', 'Announcements'), 
        ('contact', 'Contact'),  # ✅ ADD THIS
    ]

    section = models.CharField(max_length=50, choices=SECTION_CHOICES, unique=True)
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='breadcrumbs/sections/')

    def __str__(self):
        return self.get_section_display()


# ==================================================
# WHY CHOOSE US
# ==================================================
class WhyChooseUs(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    breadcrumb_image = models.ImageField(
        upload_to='breadcrumbs/why_choose_us/',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# ==================================================
# DIRECTOR MESSAGE
# ==================================================
class DirectorMessage(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=150)
    photo = models.ImageField(upload_to="director/")
    message = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# morning
# ==================================================
# CONTACT PAGE
# ==================================================
class ContactPage(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    image = models.ImageField(
        upload_to='contact/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or "Contact Page"
    
# ==================================================
# CONTACT MESSAGES
# ==================================================
class ContactMessage(models.Model):

    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    is_read = models.BooleanField(default=False)   # 👈 NEW FIELD

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"{self.name} - {self.subject}"

# Annoncements
    
# class Announcement(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title
# ==================================================
# ANNOUNCEMENT CATEGORY
# ==================================================
class AnnouncementCategory(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Announcement Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ==================================================
# ANNOUNCEMENTS
# ==================================================
class Announcement(models.Model):
    category = models.ForeignKey(
        AnnouncementCategory,
        on_delete=models.CASCADE,
        related_name="announcements"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(
        upload_to="announcements/pdfs/",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title



# ==================================================
# Leadership
# ==================================================

class LeadershipMessage(models.Model):
    name = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='leadership/')
    message = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    # Footer section
class FooterSection(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Footer Section"
        verbose_name_plural = "Footer Sections"

    def __str__(self):
        return self.name


class FooterLink(models.Model):
    section = models.ForeignKey(
        FooterSection,
        on_delete=models.CASCADE,
        related_name="links"
    )
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Footer Link"
        verbose_name_plural = "Footer Links"

    def __str__(self):
        return self.title
    
class SitePage(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



# ==================================================
# COURSE SYLLABUS
# ==================================================
class CourseSyllabus(models.Model):
    class Meta:
        db_table = 't_course_syllabus'
        verbose_name_plural = 'COURSE SYLLABUS'

    course = models.OneToOneField(
        CoursesModel,
        on_delete=models.CASCADE,
        related_name='syllabus'
    )

    title = models.CharField(max_length=200, default="Course Syllabus")

    content = models.TextField(
        help_text="Add full syllabus content here"
    )

    pdf_file = models.FileField(
        upload_to='courses/syllabus/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.course.heads} - Syllabus"