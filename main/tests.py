from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.core.exceptions import ImproperlyConfigured
from unittest.mock import patch
from pathlib import Path
import os
import runpy
from main.views import PORTFOLIO_DISPLAY_NAME
from django.template.loader import render_to_string
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.utils import timezone
from main.models import Organization, Education

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
        self.assertContains(response, 'id="organization-grid"')
        data = self.client.get(reverse("main:get_organizations_json")).json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["pk"], str(self.organization.pk))
        for field in ("title", "desc_1", "desc_2", "desc_3", "category"):
            self.assertEqual(data[0]["fields"][field], getattr(self.organization, field))
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_organization_page(self):
        Organization.objects.all().delete()
        response = self.client.get(reverse("main:show_organization"))
        self.assertContains(response, "Belum ada organization yang ditambahkan atau ditemukan.")
        self.assertEqual(self.client.get(reverse("main:get_organizations_json")).json(), [])

    def test_completed_organization(self):
        self.organization.ended_at = timezone.now()
        self.organization.save()
        self.assertFalse(self.organization.is_ongoing)

    def test_education_url_and_template(self):
        response = self.client.get(reverse('main:show_education'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'education.html')

    def test_education_empty_message(self):
        response = self.client.get(reverse('main:show_education'))
        self.assertContains(response, "Belum ada education yang ditambahkan atau ditemukan.")
        self.assertEqual(self.client.get(reverse("main:get_educations_json")).json(), [])

    def test_education_data_displayed(self):
        Education.objects.create(
            school_name="Universitas Indonesia",
            degree="S1 Sistem Informasi",
            start_year="2024",
            end_year="2028"
        )
        response = self.client.get(reverse('main:show_education'))
        self.assertContains(response, 'id="education-grid"')
        data = self.client.get(reverse("main:get_educations_json")).json()
        self.assertEqual(len(data), 1)
        fields = data[0]["fields"]
        self.assertEqual(fields["school_name"], "Universitas Indonesia")
        self.assertEqual(fields["degree"], "S1 Sistem Informasi")
        self.assertEqual(fields["start_year"], "2024")
        self.assertEqual(fields["end_year"], "2028")

class StabilizationTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user("owner", is_superuser=True)
        self.editor = User.objects.create_user("editor")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.viewer = User.objects.create_user("viewer")
        self.organization = Organization.objects.create(title="Original", category="Club")
        self.education = Education.objects.create(school_name="School", degree="BSc", start_year="2024")
        self.org_data = {"title": "Updated", "category": "Club", "desc_1": "Description"}
        self.edu_data = {"school_name": "Updated School", "degree": "BSc", "start_year": "2024"}

    def test_update_forms_preserve_record_for_editor_and_superuser(self):
        for user in (self.editor, self.owner):
            self.client.force_login(user)
            for kind, obj, payload, model in (
                ("organization", self.organization, self.org_data, Organization),
                ("education", self.education, self.edu_data, Education),
            ):
                with self.subTest(user=user.username, kind=kind):
                    url = reverse(f"main:update_{kind}", args=[obj.pk])
                    response = self.client.get(url)
                    self.assertContains(response, f'action="{url}"')
                    self.assertEqual(response.context["name"], PORTFOLIO_DISPLAY_NAME)
                    self.assertContains(response, f"Update {kind.title()}")
                    original_pk = obj.pk
                    self.assertRedirects(self.client.post(url, payload), reverse(f"main:show_{kind}"))
                    obj.refresh_from_db()
                    self.assertEqual(obj.pk, original_pk)
                    self.assertEqual(model.objects.count(), 1)
                    for field, value in payload.items():
                        self.assertEqual(getattr(obj, field), value)

    def test_create_forms_use_create_mode_even_with_default_uuid(self):
        self.client.force_login(self.owner)

        for kind in ("organization", "education"):
            url = reverse(f"main:create_{kind}")
            response = self.client.get(url)

            self.assertContains(response, f'action="{url}"')
            self.assertEqual(response.context["name"], PORTFOLIO_DISPLAY_NAME)

            expected_title = (
                "Add New Organization"
                if kind == "organization"
                else "Add Education"
            )

            self.assertContains(response, expected_title)
            self.assertNotContains(response, f"Update {kind.title()}")

    def test_create_and_update_reject_unsupported_methods(self):
        self.client.force_login(self.owner)
        for kind, obj in (("organization", self.organization), ("education", self.education)):
            for name, args in (("create", []), ("update", [obj.pk])):
                self.assertEqual(self.client.put(reverse(f"main:{name}_{kind}", args=args)).status_code, 405)

    def test_role_boundaries_for_mutations(self):
        for user in (self.viewer, self.editor):
            self.client.force_login(user)
            for kind, obj, payload in (("organization", self.organization, self.org_data), ("education", self.education, self.edu_data)):
                for suffix in ("", "_ajax"):
                    self.assertEqual(self.client.post(reverse(f"main:create_{kind}{suffix}"), payload).status_code, 403)
                self.assertEqual(self.client.post(reverse(f"main:delete_{kind}", args=[obj.pk])).status_code, 403)
                if user == self.viewer:
                    self.assertEqual(self.client.post(reverse(f"main:update_{kind}", args=[obj.pk]), payload).status_code, 403)
        self.assertEqual(Organization.objects.count(), 1)
        self.assertEqual(Education.objects.count(), 1)

    def test_star_csrf_initialization_rejection_toggle_and_json(self):
        for kind, obj, star_name, api_name in (
            ("organization", self.organization, "toggle_star", "get_organizations_json"),
            ("education", self.education, "toggle_star_education", "get_educations_json"),
        ):
            with self.subTest(kind=kind):
                client = Client(enforce_csrf_checks=True)
                client.force_login(self.viewer)
                response = client.get(reverse(f"main:show_{kind}"))
                self.assertIn("csrftoken", response.cookies)
                url = reverse(f"main:{star_name}", args=[obj.pk])
                self.assertEqual(client.post(url).status_code, 403)
                self.assertEqual(obj.starred_by.count(), 0)
                token = client.cookies["csrftoken"].value
                self.assertEqual(client.post(url, HTTP_X_CSRFTOKEN="invalid").status_code, 403)
                for expected, count in (("starred", 1), ("unstarred", 0)):
                    response = client.post(url, HTTP_X_CSRFTOKEN=token)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.json()["status"], expected)
                    self.assertEqual(obj.starred_by.count(), count)
                    fields = client.get(reverse(f"main:{api_name}")).json()[0]["fields"]
                    self.assertEqual(fields["star_count"], count)
                    self.assertEqual(fields["is_starred"], bool(count))

    def test_post_only_endpoints_and_delete(self):
        self.client.force_login(self.owner)
        urls = [reverse("main:logout")]
        for kind, obj, star in (("organization", self.organization, "toggle_star"), ("education", self.education, "toggle_star_education")):
            urls.extend([reverse(f"main:delete_{kind}", args=[obj.pk]), reverse(f"main:{star}", args=[obj.pk]), reverse(f"main:create_{kind}_ajax")])
        for url in urls:
            for method in ("get", "put", "delete"):
                self.assertEqual(getattr(self.client, method)(url).status_code, 405)
        self.assertTrue(Organization.objects.filter(pk=self.organization.pk).exists())
        self.assertTrue(Education.objects.filter(pk=self.education.pk).exists())
        for kind, obj in (("organization", self.organization), ("education", self.education)):
            self.assertRedirects(self.client.post(reverse(f"main:delete_{kind}", args=[obj.pk])), reverse(f"main:show_{kind}"))
            self.assertFalse(type(obj).objects.filter(pk=obj.pk).exists())

    def test_logout_post_removes_session_and_last_login(self):
        self.client.force_login(self.viewer)
        self.client.cookies["last_login"] = "test"
        response = self.client.post(reverse("main:logout"))
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(response.cookies["last_login"]["max-age"], 0)

    def test_search_json_filters(self):
        for api, query, expected in (("get_organizations_json", "original", str(self.organization.pk)), ("get_educations_json", "school", str(self.education.pk))):
            response = self.client.get(reverse(f"main:{api}"), {"title": query})
            self.assertEqual(response.status_code, 200)
            self.assertEqual([item["pk"] for item in response.json()], [expected])
            self.assertEqual(self.client.get(reverse(f"main:{api}"), {"title": "no-match"}).json(), [])

    def test_guest_cannot_mutate(self):
        for kind, obj, payload, star in (("organization", self.organization, self.org_data, "toggle_star"), ("education", self.education, self.edu_data, "toggle_star_education")):
            for name, args in ((f"create_{kind}", []), (f"update_{kind}", [obj.pk]), (f"delete_{kind}", [obj.pk]), (star, [obj.pk])):
                self.assertEqual(self.client.post(reverse(f"main:{name}", args=args), payload).status_code, 302)
            self.assertEqual(self.client.post(reverse(f"main:create_{kind}_ajax"), payload).status_code, 403)
        self.assertEqual(Organization.objects.count(), 1)
        self.assertEqual(Education.objects.count(), 1)
        self.assertEqual(self.organization.starred_by.count(), 0)
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_delete_and_logout_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        for kind, obj in (("organization", self.organization), ("education", self.education)):
            url = reverse(f"main:delete_{kind}", args=[obj.pk])
            self.assertEqual(client.post(url).status_code, 403)
            self.assertTrue(type(obj).objects.filter(pk=obj.pk).exists())
        self.assertEqual(client.post(reverse("main:logout")).status_code, 403)
        self.assertIn("_auth_user_id", client.session)


    def test_display_name_and_navigation_across_public_pages_and_roles(self):
        for user in (None, self.viewer, self.editor, self.owner):
            self.client.logout()
            if user:
                self.client.force_login(user)
            for page in ("show_main", "show_organization", "show_education", "login", "register"):
                with self.subTest(user=user, page=page):
                    response = self.client.get(reverse(f"main:{page}"))
                    self.assertEqual(response.context["name"], "Jotham Seanvedi")
                    self.assertContains(response, 'class="brand">Jotham Seanvedi</a>')
                    self.assertContains(response, "2026 Jotham Seanvedi.")
                    self.assertNotContains(response, "Takin Allo")
                    self.assertIn("Jotham Seanvedi", response.content.decode().split("<title>")[1].split("</title>")[0])
                    if user:
                        self.assertContains(response, f'action="{reverse("main:logout")}"')
                        navigation = response.content.decode().split("<nav>")[1].split("</nav>")[0]
                        self.assertNotIn(f'href="{reverse("main:login")}"', navigation)
                        self.assertNotIn(f'href="{reverse("main:register")}"', navigation)
                    else:
                        self.assertContains(response, f'href="{reverse("main:login")}"')
                        self.assertContains(response, f'href="{reverse("main:register")}"')
                        self.assertNotContains(response, f'action="{reverse("main:logout")}"')

    def test_guest_never_sees_stale_last_login(self):
        self.client.cookies["last_login"] = "stale-cookie-timestamp"
        response = self.client.get(reverse("main:show_main"))
        self.assertIsNone(response.context["last_login"])
        self.assertNotContains(response, "Last Login")
        self.assertNotContains(response, "stale-cookie-timestamp")

    def test_authenticated_last_login_uses_account_timestamp_not_cookie(self):
        self.client.force_login(self.viewer)
        self.viewer.refresh_from_db()
        for cookie in (None, "stale-cookie-timestamp"):
            if cookie is None:
                self.client.cookies.pop("last_login", None)
            else:
                self.client.cookies["last_login"] = cookie
            response = self.client.get(reverse("main:show_main"))
            self.assertEqual(response.context["last_login"], self.viewer.last_login)
            self.assertContains(response, "Last Login (account)")
            self.assertContains(response, timezone.localtime(self.viewer.last_login).strftime("%Y-%m-%d %H:%M:%S %z"))
            self.assertNotContains(response, "stale-cookie-timestamp")
        self.client.post(reverse("main:logout"))
        self.assertNotContains(self.client.get(reverse("main:show_main")), "Last Login")

    def test_login_keeps_coursework_cookie_and_session(self):
        # Exercise the successful login view without storing test credentials.
        with patch("main.views.AuthenticationForm") as form_class:
            form_class.return_value.is_valid.return_value = True
            form_class.return_value.get_user.return_value = self.viewer
            response = self.client.post(reverse("main:login"), {"username": self.viewer.username})
        self.viewer.refresh_from_db()
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertEqual(response.cookies["last_login"].value, self.viewer.last_login.isoformat())
        self.assertEqual(self.client.session["_auth_user_id"], str(self.viewer.pk))

    def test_guest_star_json_and_legacy_component_are_read_only(self):
        for kind, obj, api in (("organization", self.organization, "get_organizations_json"), ("education", self.education, "get_educations_json")):
            obj.starred_by.add(self.viewer)
            fields = self.client.get(reverse(f"main:{api}")).json()[0]["fields"]
            self.assertEqual(fields["star_count"], 1)
            self.assertFalse(fields["is_starred"])
            response = self.client.get(reverse(f"main:show_{kind}"))
            self.assertContains(response, 'class="star-count"')
            self.assertContains(response, 'const IS_AUTHENTICATED = "false" === "true";')
        component = render_to_string("components/organization_star.html", {"organization": self.organization, "user": AnonymousUser()})
        self.assertIn("Stars: 1", component)
        self.assertNotIn("<button", component)
        self.assertNotIn("<a", component)

    def test_star_state_and_page_permissions_for_all_roles(self):
        for obj in (self.organization, self.education):
            obj.starred_by.add(self.viewer)
        for user in (None, self.viewer, self.editor, self.owner):
            self.client.logout()
            if user:
                self.client.force_login(user)
            for kind, obj, api in (("organization", self.organization, "get_organizations_json"), ("education", self.education, "get_educations_json")):
                with self.subTest(user=user, kind=kind):
                    response = self.client.get(reverse(f"main:show_{kind}"))
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.context["is_editor"], user == self.editor)
                    authenticated = "true" if user else "false"
                    self.assertContains(response, f'const IS_AUTHENTICATED = "{authenticated}" === "true";')
                    if user == self.owner:
                        self.assertContains(response, f'id="add-{kind}-modal"')
                    else:
                        self.assertNotContains(response, f'id="add-{kind}-modal"')
                    data = self.client.get(reverse(f"main:{api}")).json()
                    self.assertEqual(len(data), 1)
                    self.assertEqual(data[0]["pk"], str(obj.pk))
                    self.assertEqual(data[0]["fields"]["star_count"], 1)
                    self.assertEqual(data[0]["fields"]["is_starred"], user == self.viewer)


class ConfigurationTest(TestCase):
    def load_settings(self, values):
        path = Path(__file__).resolve().parents[1] / "portofolio" / "settings.py"
        with patch.dict(os.environ, values, clear=True), patch("dotenv.load_dotenv"):
            return runpy.run_path(str(path))

    def test_missing_secret_fails_without_exposing_a_value(self):
        with self.assertRaises(ImproperlyConfigured):
            self.load_settings({"PRODUCTION": "True"})

    def test_debug_defaults_and_production_guard(self):
        # Dummy key belongs only to this isolated configuration test.
        values = {"SECRET_KEY": "configuration-test-placeholder"}
        self.assertTrue(self.load_settings(values)["DEBUG"])
        self.assertFalse(self.load_settings({**values, "DEBUG": "False"})["DEBUG"])
        self.assertFalse(self.load_settings({**values, "PRODUCTION": "True"})["DEBUG"])
        with self.assertRaises(ImproperlyConfigured):
            self.load_settings({**values, "PRODUCTION": "True", "DEBUG": "True"})
