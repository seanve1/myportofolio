import uuid
from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase

from main.models import Organization
from main.serializers import OrganizationSerializer


class OrganizationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user("api-owner", is_superuser=True)
        self.visitor = User.objects.create_user("api-visitor")
        self.editor = User.objects.create_user("api-editor")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.staff = User.objects.create_user("api-staff", is_staff=True)
        self.organization = Organization.objects.create(
            title="Portfolio Club", category="Community", desc_1="Original description",
        )
        self.list_url = reverse("api:organization-list")
        self.detail_url = reverse("api:organization-detail", args=[self.organization.pk])
        self.star_url = reverse("api:organization-star", args=[self.organization.pk])
        self.payload = {"title": "New organization", "category": "Student club", "desc_1": "Activities"}

    def test_public_list_and_detail(self):
        self.organization.starred_by.add(self.visitor)
        for url in (self.list_url, self.detail_url):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            data = response.data[0] if url == self.list_url else response.data
            self.assertEqual(data["id"], str(self.organization.pk))
            self.assertEqual(data["title"], self.organization.title)
            self.assertEqual(data["star_count"], 1)
            self.assertFalse(data["is_starred"])
            self.assertEqual(data["starred_by_names"], self.visitor.username)
            self.assertNotIn("fields", data)
            self.assertNotIn("starred_by", data)
            self.assertEqual(set(data), set(OrganizationSerializer.Meta.fields))

    def test_search_empty_results_and_ordering(self):
        first = Organization.objects.create(title="Alpha", category="Group")
        self.assertEqual(self.client.get(self.list_url).data[0]["id"], str(first.pk))
        response = self.client.get(self.list_url, {"title": "  PORTFOLIO  "})
        self.assertEqual([item["id"] for item in response.data], [str(self.organization.pk)])
        self.assertEqual(self.client.get(self.list_url, {"title": "not-found"}).data, [])

    def test_missing_organization(self):
        self.assertEqual(self.client.get(reverse("api:organization-detail", args=[uuid.uuid4()])).status_code, 404)
        self.client.force_authenticate(self.owner)
        self.assertEqual(self.client.post(reverse("api:organization-star", args=[uuid.uuid4()])).status_code, 404)

    def test_guest_regular_and_staff_cannot_manage(self):
        for user in (None, self.visitor, self.staff):
            self.client.force_authenticate(user=user)
            for method, url, payload in (
                ("post", self.list_url, self.payload),
                ("put", self.detail_url, self.payload),
                ("patch", self.detail_url, {"title": "Forbidden"}),
                ("delete", self.detail_url, {}),
            ):
                with self.subTest(user=user, method=method):
                    self.assertEqual(getattr(self.client, method)(url, payload, format="json").status_code, 403)
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.title, "Portfolio Club")
        self.assertEqual(Organization.objects.count(), 1)

    def test_owner_can_create_and_clean_text(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "title": " <b>New club</b> ", "category": "<b>Club</b>",
            "desc_1": "<b>One</b>", "desc_2": "<i>Two</i>", "desc_3": "<p>Three</p>",
            "thumbnail": "https://example.com/logo.png",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        organization = Organization.objects.get(pk=response.data["id"])
        self.assertEqual(organization.title, "New club")
        self.assertEqual(organization.category, "Club")
        self.assertEqual((organization.desc_1, organization.desc_2, organization.desc_3), ("One", "Two", "Three"))

    def test_validation_rejects_bad_input_without_writes(self):
        self.client.force_authenticate(self.owner)
        for changes, field in (
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"category": "<b></b>"}, "category"),
            ({"title": "x" * 256}, "title"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
            ({"started_at": "invalid-date"}, "started_at"),
        ):
            with self.subTest(field=field, changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)
        self.assertEqual(Organization.objects.count(), 1)

    def test_patch_put_and_delete_preserve_uuid_and_relations(self):
        self.client.force_authenticate(self.owner)
        self.organization.starred_by.add(self.visitor)
        original_pk = self.organization.pk
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.desc_1, "Original description")
        self.assertEqual(self.organization.pk, original_pk)
        self.assertEqual(self.client.put(self.detail_url, {"title": "Incomplete"}, format="json").status_code, 400)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.pk, original_pk)
        self.assertEqual(self.organization.title, self.payload["title"])
        self.assertTrue(self.organization.starred_by.filter(pk=self.visitor.pk).exists())
        self.assertEqual(Organization.objects.count(), 1)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Organization.objects.filter(pk=original_pk).exists())

    def test_editor_can_update_but_not_create_or_delete(self):
        self.client.force_authenticate(self.editor)
        self.assertEqual(self.client.patch(self.detail_url, {"title": "Editor update"}, format="json").status_code, 200)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.title, self.payload["title"])
        self.assertEqual(Organization.objects.count(), 1)

    def test_star_requires_login_and_toggles_current_user_only(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assertEqual(self.client.get(self.star_url).status_code, 403)
        for user in (self.visitor, self.editor, self.owner):
            self.client.force_authenticate(user)
            for expected, count in ((True, 1), (False, 0)):
                response = self.client.post(self.star_url, {"user_id": self.staff.pk}, format="json")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["is_starred"], expected)
                self.assertEqual(response.data["star_count"], count)
                self.assertEqual(self.organization.starred_by.filter(pk=user.pk).exists(), expected)
                self.assertFalse(self.organization.starred_by.filter(pk=self.staff.pk).exists())
                self.assertEqual(response.data["starred_by_names"], user.username if expected else "")

    def test_computed_fields_and_id_are_read_only(self):
        self.client.force_authenticate(self.owner)
        forged_id = uuid.uuid4()
        response = self.client.post(self.list_url, {
            **self.payload, "id": str(forged_id), "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.pk],
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], str(forged_id))
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")
        self.assertEqual(Organization.objects.get(pk=response.data["id"]).starred_by.count(), 0)

    def test_wrong_methods_and_safe_methods_do_not_mutate(self):
        self.client.force_authenticate(self.owner)
        for url, method in ((self.list_url, "delete"), (self.list_url, "patch"), (self.detail_url, "post"), (self.star_url, "get")):
            self.assertEqual(getattr(self.client, method)(url).status_code, 405)
        for url in (self.list_url, self.detail_url):
            self.assertEqual(self.client.head(url).status_code, 200)
            self.assertEqual(self.client.options(url).status_code, 200)
        self.assertEqual(Organization.objects.count(), 1)
        self.assertEqual(self.organization.starred_by.count(), 0)

    def test_session_mutations_without_or_with_invalid_csrf_are_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.owner)
        client.get(reverse("main:show_organization"))
        for method, url, payload in (
            ("post", self.list_url, self.payload), ("put", self.detail_url, self.payload),
            ("patch", self.detail_url, {"title": "CSRF attempt"}),
            ("delete", self.detail_url, {}), ("post", self.star_url, {}),
        ):
            for headers in ({}, {"HTTP_X_CSRFTOKEN": "invalid"}):
                with self.subTest(method=method, url=url, headers=bool(headers)):
                    self.assertEqual(getattr(client, method)(url, payload, format="json", **headers).status_code, 403)
        self.assertEqual(Organization.objects.count(), 1)
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.title, "Portfolio Club")
        self.assertEqual(self.organization.starred_by.count(), 0)

    def test_session_mutations_with_csrf_succeed(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.owner)
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, 200)
        self.assertIn("csrftoken", client.cookies)
        headers = {"HTTP_X_CSRFTOKEN": client.cookies["csrftoken"].value}
        self.assertEqual(client.post(self.list_url, self.payload, format="json", **headers).status_code, 201)
        self.assertEqual(client.put(self.detail_url, self.payload, format="json", **headers).status_code, 200)
        self.assertEqual(client.patch(self.detail_url, {"title": "Session update"}, format="json", **headers).status_code, 200)
        self.assertTrue(client.post(self.star_url, **headers).data["is_starred"])
        self.assertEqual(client.delete(self.detail_url, **headers).status_code, 204)

    def test_dates_validate_partial_updates_and_allow_optional_nulls(self):
        self.client.force_authenticate(self.owner)
        start = timezone.now()
        self.organization.started_at = start
        self.organization.ended_at = start + timedelta(days=2)
        self.organization.save()
        for changes in (
            {"ended_at": (start - timedelta(days=1)).isoformat()},
            {"started_at": (start + timedelta(days=3)).isoformat()},
        ):
            response = self.client.patch(self.detail_url, changes, format="json")
            self.assertEqual(response.status_code, 400)
            self.assertIn("ended_at", response.data)
        response = self.client.patch(self.detail_url, {
            "ended_at": None, "desc_1": None, "desc_2": "", "desc_3": None, "thumbnail": "",
        }, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data["ended_at"])
        self.assertIsNone(response.data["desc_1"])

    def test_serializer_without_request_and_permission_before_lookup(self):
        self.organization.starred_by.add(self.visitor)
        self.assertFalse(OrganizationSerializer(self.organization).data["is_starred"])
        missing = reverse("api:organization-detail", args=[uuid.uuid4()])
        self.client.force_authenticate(self.visitor)
        self.assertEqual(self.client.patch(missing, {"title": "Denied"}, format="json").status_code, 403)

    def test_malformed_json_is_rejected(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, '{"title":', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Organization.objects.count(), 1)

    def test_organization_page_and_ajax_session_contract_for_all_roles(self):
        for user in (None, self.visitor, self.editor, self.owner):
            with self.subTest(user=user):
                client = APIClient(enforce_csrf_checks=True)
                if user:
                    client.force_login(user)
                page = client.get(reverse("main:show_organization"))
                self.assertEqual(page.status_code, 200)
                self.assertContains(page, f'const BASE_ORGANIZATIONS_ENDPOINT = "{self.list_url}";')
                self.assertContains(page, 'const DETAIL_ORGANIZATION_ENDPOINT = "/api/v1/organizations/')
                self.assertContains(page, 'const STAR_ORGANIZATION_ENDPOINT = "/api/v1/organizations/')
                self.assertNotContains(page, "item.fields")
                self.assertNotContains(page, "item.pk")
                self.assertIn("csrftoken", client.cookies)
                headers = {"HTTP_X_CSRFTOKEN": client.cookies["csrftoken"].value}
                self.assertEqual(client.get(self.list_url, HTTP_ACCEPT="application/json").status_code, 200)
                response = client.post(self.star_url, format="json", **headers)
                self.assertEqual(response.status_code, 200 if user else 403)
                if user:
                    self.assertTrue(response.data["is_starred"])
                    self.assertFalse(client.post(self.star_url, **headers).data["is_starred"])
                response = client.patch(self.detail_url, {"title": "Session update"}, format="json", **headers)
                self.assertEqual(response.status_code, 200 if user in (self.editor, self.owner) else 403)
                response = client.post(self.list_url, {
                    **self.payload, "started_at": None, "ended_at": None,
                }, format="json", **headers)
                self.assertEqual(response.status_code, 201 if user == self.owner else 403)
                if user == self.owner:
                    created_url = reverse("api:organization-detail", args=[response.data["id"]])
                    deleted = client.delete(created_url, **headers)
                    self.assertEqual(deleted.status_code, 204)
                    self.assertEqual(deleted.content, b"")
