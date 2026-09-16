from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Organization, Education
from .forms import OrganizationForm


def show_main(request):
    context = {
        "name": "Jotham Seanvedi Takin Allo",
        "npm": "2506584161",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "A highly motivated learner with a strong passion for mathematics and technology, "
            "currently pursuing Information Systems at Universitas Indonesia. "
            "I am someone who is always eager to learn, persistent in every effort, and forward-looking in seeking opportunities for growth. "
            "With a mindset focused on continuous improvement, I embrace challenges as chances to develop myself and contribute meaningfully in both academic and professional fields"
        ),
    }
    return render(request, "index.html", context)


def show_organization(request):
    json_response = get_organizations_json(request)

    organizations = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )

    organizations = [organization.object for organization in organizations]

    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Jotham Seanvedi Takin Allo",
        "organization_list": organizations,
        "title_query": title_query,
    }

    return render(request, "organization.html", context)

def show_education(request):
    data = Education.objects.all()
    context = {
        'name': 'Jotham Seanvedi',
        'educations': data
    }
    return render(request, "education.html", context)

def create_organization(request):
    form = OrganizationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Organisasi baru berhasil ditambahkan!")
        return redirect("main:show_organization")

    context = {
        "name": "Jotham Seanvedi Takin Allo",
        "form": form,
    }

    return render(request, "organization_form.html", context)

def get_organizations_json(request):
    title_query = request.GET.get("title", "").strip()

    organizations = Organization.objects.all()

    if title_query:
        organizations = organizations.filter(title__icontains=title_query)

    organizations_json = serializers.serialize("json", organizations)

    return HttpResponse(
        organizations_json,
        content_type="application/json"
    )

def delete_organization(request, organization_id):
    organization = get_object_or_404(
        Organization,
        pk=organization_id
    )

    if request.method == "POST":
        organization.delete()

        messages.success(
            request,
            "Organization berhasil dihapus!"
        )

        return redirect("main:show_organization")

    return redirect("main:show_organization")