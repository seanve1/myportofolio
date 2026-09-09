from django.shortcuts import render

from main.models import Experience


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


def show_experience(request):
    context = {
        "name": "Jotham Seanvedi Takin Allo",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)