from django.forms import ModelForm, TextInput, Textarea, URLInput, DateTimeInput
from django.utils.html import strip_tags
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

    def clean_title(self):
        title = self.cleaned_data["title"]
        return strip_tags(title)

    def clean_category(self):
        category = self.cleaned_data["category"]
        return strip_tags(category)

    def clean_desc_1(self):
        desc_1 = self.cleaned_data["desc_1"]
        return strip_tags(desc_1)

    def clean_desc_2(self):
        desc_2 = self.cleaned_data.get("desc_2", "")
        return strip_tags(desc_2) if desc_2 else ""

    def clean_desc_3(self):
        desc_3 = self.cleaned_data.get("desc_3", "")
        return strip_tags(desc_3) if desc_3 else ""

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
        
    def clean_school_name(self):
        school_name = self.cleaned_data["school_name"]
        return strip_tags(school_name)

    def clean_degree(self):
        degree = self.cleaned_data["degree"]
        return strip_tags(degree)

    def clean_start_year(self):
        start_year = self.cleaned_data["start_year"]
        return strip_tags(start_year)

    def clean_end_year(self):
        end_year = self.cleaned_data.get("end_year", "")
        return strip_tags(end_year) if end_year else ""