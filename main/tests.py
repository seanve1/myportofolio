from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from main.models import Organization

class MainTest(TestCase):
    def setUp(self):
        # Membuat data sampel pengalaman untuk keperluan pengujian
        self.organization = Organization.objects.create(
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
        self.assertNotContains(response, self.organization.title)
        self.assertContains(response, f'href="{reverse("main:show_organization")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_organization_model(self):
        self.assertEqual(str(self.organization), "Asisten Dosen PBP")
        self.assertEqual(self.organization.category, "Fasilkom UI")
        self.assertTrue(self.organization.is_ongoing)

    def test_organization_page(self):
        response = self.client.get(reverse("main:show_organization"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "organization.html")
        self.assertContains(response, self.organization.title)
        self.assertContains(response, self.organization.desc_1)
        self.assertContains(response, self.organization.category)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_organization_page(self):
        Organization.objects.all().delete()
        response = self.client.get(reverse("main:show_organization"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_organization(self):
        self.organization.ended_at = timezone.now()
        self.organization.save()
        self.assertFalse(self.organization.is_ongoing)