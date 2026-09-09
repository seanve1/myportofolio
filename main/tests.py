from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from main.models import Experience

class MainTest(TestCase):
    def setUp(self):
        # Membuat data sampel pengalaman untuk keperluan pengujian
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            category="Fasilkom UI",
            desc_1="Membantu mahasiswa memahami dasar pengembangan web.",
            desc_2="Mengoreksi tugas dan memberikan penilaian.",
            desc_3="Menjaga sesi konsultasi mahasiswa.",
            started_at=timezone.now()
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "Fasilkom UI")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.desc_1)
        self.assertContains(response, self.experience.category)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        self.assertFalse(self.experience.is_ongoing)