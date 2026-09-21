from django.forms import ModelForm, TextInput, Textarea, URLInput, DateTimeInput

from main.models import Organization, Education

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization

        fields = [
            "title",
            "category",
            "desc_1",
            "desc_2",
            "desc_3",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Organization Position",
            "category": "Organization Name",
            "desc_1": "1st Description",
            "desc_2": "2nd Description",
            "desc_3": "3rd Description",
            "thumbnail": "URL Logo",
            "started_at": "Start Date",
            "ended_at": "End Date",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Staff of ...",
                    "maxlength": 255,
                }
            ),

            "category": TextInput(
                attrs={
                    "placeholder": "Nama organisasi",
                    "maxlength": 255,
                }
            ),

            "desc_1": Textarea(
                attrs={
                    "placeholder": "The first description or responsibility",
                    "rows": 3,
                }
            ),

            "desc_2": Textarea(
                attrs={
                    "placeholder": "The second description or responsibility",
                    "rows": 3,
                }
            ),

            "desc_3": Textarea(
                attrs={
                    "placeholder": "The third description or responsibility",
                    "rows": 3,
                }
            ),

            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/logo.png",
                }
            ),

            "started_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),

            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }

class EducationForm (ModelForm):
    class Meta:
        model = Education

        fields = [
            "school_name",
            "degree",
            "start_year",
            "end_year",
            "logo",
        ]

        labels = {
            "school_name": "School Name",
            "degree": "Degree",
            "start_year": "Start Year",
            "end_year": "End Year",
            "logo": "Logo URL",
        }

        widgets = {
            "school_name": TextInput(
                attrs={
                    "placeholder": "Universitas Indonesia",
                    "maxlength": 255,
                }
            ),

            "degree": TextInput(
                attrs={
                    "placeholder": "S1 Sistem Informasi",
                    "maxlength": 255,
                }
            ),

            "start_year": TextInput(
                attrs={
                    "placeholder": "2025",
                    "maxlength": 4,
                }
            ),

            "end_year": TextInput(
                attrs={
                    "placeholder": "2029",
                    "maxlength": 4,
                }
            ),

            "logo": URLInput(
                attrs={
                    "placeholder": "https://example.com/logo.png",
                }
            ),
        }