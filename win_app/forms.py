from django import forms
from .models import Administration, Event, Application
import re
from datetime import date




# ==================================================
# ADMINISTRATION FORM
# ==================================================
class AdministrationForm(forms.ModelForm):
    class Meta:
        model = Administration
        fields = ['name', 'designation', 'department', 'photo', 'details']


# ==================================================
# EVENT FORM
# ==================================================
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'


# ==================================================
# APPLICATION FORM
# ==================================================
class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = [

            # Student
            'first_name',
            'middle_name',
            'last_name',

            'program',
            'dob',
            'gender',

            # Father
            'father_first_name',
            'father_middle_name',
            'father_last_name',

            # Mother
            'mother_first_name',
            'mother_middle_name',
            'mother_last_name',

            'address',
            'contact_number',
            'email',
            'photo',
            'document',
            'agree',
        ]

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),

            'gender': forms.RadioSelect(choices=[
                ('male', 'Male'),
                ('female', 'Female'),
                ('other', 'Others')
            ]),

            'agree': forms.CheckboxInput(),
        }

    # --------------------------------------------------
    # INIT (Styling + Placeholders)
    # --------------------------------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 🔴 REMOVE -------- OPTION
        self.fields['gender'].choices = [
                        ('male', 'Male'),
                        ('female', 'Female'),
                        ('other', 'Others'),
                    ]

        for field in self.fields.values():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})

        # Student
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['middle_name'].widget.attrs.update({'placeholder': 'Middle Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})

        # Father
        self.fields['father_first_name'].widget.attrs.update({'placeholder': 'Father First Name'})
        self.fields['father_middle_name'].widget.attrs.update({'placeholder': 'Father Middle Name'})
        self.fields['father_last_name'].widget.attrs.update({'placeholder': 'Father Last Name'})

        # Mother
        self.fields['mother_first_name'].widget.attrs.update({'placeholder': 'Mother First Name'})
        self.fields['mother_middle_name'].widget.attrs.update({'placeholder': 'Mother Middle Name'})
        self.fields['mother_last_name'].widget.attrs.update({'placeholder': 'Mother Last Name'})

        # Program select placeholder
        self.fields['program'].choices = [('', 'Select')] + list(self.fields['program'].choices)[1:]

        # Phone number
        self.fields['contact_number'].widget.attrs.update({
            'placeholder': '10-digit Mobile Number',
            'maxlength': '10',
            'oninput': 'this.value=this.value.replace(/[^0-9]/g,"")'
        })

    # --------------------------------------------------
    # NAME VALIDATION
    # --------------------------------------------------
    def _validate_name(self, name, field):

        if not name:
            raise forms.ValidationError(f"{field} is required")

        name = name.strip()

        if len(name) < 2:
            raise forms.ValidationError(f"{field} must be at least 2 characters")

        if not re.match(r"^[A-Za-z\s'-]+$", name):
            raise forms.ValidationError(
                f"{field} can contain only letters, spaces, hyphens or apostrophes"
            )

        if len(set(name.lower().replace(" ", ""))) == 1:
            raise forms.ValidationError("Please enter a valid name")

        return name

    def clean_first_name(self):
        return self._validate_name(self.cleaned_data.get('first_name'), "First name")

    def clean_last_name(self):
        return self._validate_name(self.cleaned_data.get('last_name'), "Last name")

    def clean_father_first_name(self):
        return self._validate_name(self.cleaned_data.get('father_first_name'), "Father first name")

    def clean_father_last_name(self):
        return self._validate_name(self.cleaned_data.get('father_last_name'), "Father last name")

    def clean_mother_first_name(self):
        return self._validate_name(self.cleaned_data.get('mother_first_name'), "Mother first name")

    def clean_mother_last_name(self):
        return self._validate_name(self.cleaned_data.get('mother_last_name'), "Mother last name")

    # --------------------------------------------------
    # EMAIL VALIDATION
    # --------------------------------------------------
    def clean_email(self):

        email = self.cleaned_data.get('email', '').lower()

        if Application.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email has already been used for an application."
            )

        return email

    # --------------------------------------------------
    # PHONE VALIDATION
    # --------------------------------------------------
    def clean_contact_number(self):

        phone = self.cleaned_data.get('contact_number')

        if not phone or not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError(
                "Phone number must be exactly 10 digits"
            )

        if Application.objects.filter(contact_number=phone).exists():
            raise forms.ValidationError(
                "This phone number has already been used."
            )

        return phone

    # --------------------------------------------------
    # DOB VALIDATION
    # --------------------------------------------------
    def clean_dob(self):

        dob = self.cleaned_data.get('dob')
        today = date.today()

        age = (today - dob).days // 365

        if dob >= today or age < 17:
            raise forms.ValidationError(
                "Applicant must be at least 17 years old"
            )

        return dob

    # --------------------------------------------------
    # PHOTO VALIDATION
    # --------------------------------------------------
    def clean_photo(self):

        photo = self.cleaned_data.get('photo')

        if photo and photo.size > 6 * 1024 * 1024:
            raise forms.ValidationError(
                "Photo size must not exceed 6 MB"
            )

        return photo

    # --------------------------------------------------
    # DOCUMENT VALIDATION
    # --------------------------------------------------
    def clean_document(self):

        document = self.cleaned_data.get('document')

        if document:

            if not document.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are allowed.")

            if document.size > 10 * 1024 * 1024:
                raise forms.ValidationError("PDF file must not exceed 10 MB.")

        return document

    # --------------------------------------------------
    # DECLARATION CHECK
    # --------------------------------------------------
    def clean_agree(self):

        if not self.cleaned_data.get('agree'):
            raise forms.ValidationError(
                "You must accept the declaration"
            )

        return True