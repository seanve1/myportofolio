import uuid
from datetime import timedelta

from django.contrib.auth.models import AnonymousUser, Group, User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from main.models import Education, Organization
from main.serializers import EducationSerializer, OrganizationSerializer


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
        self.owner.set_password("api-csrf-test-password")
        self.owner.save(update_fields=["password"])
        self.assertTrue(client.login(username=self.owner.username, password="api-csrf-test-password"))
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
        self.owner.set_password("api-csrf-test-password")
        self.owner.save(update_fields=["password"])
        self.assertTrue(client.login(username=self.owner.username, password="api-csrf-test-password"))
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


class EducationSerializerTest(APITestCase):
    def setUp(self):
        self.visitor = User.objects.create_user("education-visitor")
        self.other_user = User.objects.create_user("education-other")
        self.education = Education.objects.create(
            school_name="Portfolio University",
            degree="Information Systems",
            start_year="2025",
            end_year="2029",
            logo="/static/img/UI.png",
        )
        self.payload = {
            "school_name": "New School",
            "degree": "Bachelor of Science",
            "start_year": "2026",
        }

    def test_serialized_fields_and_values(self):
        data = EducationSerializer(self.education).data
        self.assertEqual(data, {
            "id": str(self.education.pk),
            "school_name": "Portfolio University",
            "degree": "Information Systems",
            "start_year": "2025",
            "end_year": "2029",
            "logo": "/static/img/UI.png",
            "star_count": 0,
            "is_starred": False,
        })
        self.assertEqual(set(data), set(EducationSerializer.Meta.fields))

    def test_star_state_uses_current_request_user(self):
        self.education.starred_by.add(self.visitor)
        for user, expected in (
            (AnonymousUser(), False),
            (self.visitor, True),
            (self.other_user, False),
        ):
            with self.subTest(user=user):
                request = APIRequestFactory().get("/")
                request.user = user
                data = EducationSerializer(
                    self.education, context={"request": request}
                ).data
                self.assertEqual(data["is_starred"], expected)
                self.assertEqual(data["star_count"], 1)
        self.assertFalse(EducationSerializer(self.education).data["is_starred"])

    def test_star_count_tracks_relation_changes(self):
        for users, expected in (
            ([], 0),
            ([self.visitor], 1),
            ([self.visitor, self.other_user], 2),
            ([], 0),
        ):
            self.education.starred_by.set(users)
            self.assertEqual(
                EducationSerializer(self.education).data["star_count"], expected
            )

    def test_id_and_computed_fields_are_read_only(self):
        forged_id = uuid.uuid4()
        serializer = EducationSerializer(data={
            **self.payload,
            "id": str(forged_id),
            "star_count": 99,
            "is_starred": True,
            "starred_by": [self.visitor.pk],
        })
        for field in ("id", "star_count", "is_starred"):
            self.assertTrue(serializer.fields[field].read_only)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        for field in ("id", "star_count", "is_starred", "starred_by"):
            self.assertNotIn(field, serializer.validated_data)
        education = serializer.save()
        self.assertNotEqual(education.pk, forged_id)
        self.assertEqual(education.starred_by.count(), 0)
        self.assertEqual(serializer.data["star_count"], 0)
        self.assertFalse(serializer.data["is_starred"])

    def test_html_sanitization(self):
        serializer = EducationSerializer(data={
            **self.payload,
            "school_name": " <b>New School</b> ",
            "degree": "<i>Bachelor of Science</i>",
            "start_year": "2026",
            "end_year": "<b>",
            "logo": "<b>/static/img/UI.png</b>",
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        education = serializer.save()
        self.assertEqual(education.school_name, "New School")
        self.assertEqual(education.degree, "Bachelor of Science")
        self.assertEqual(education.start_year, "2026")
        self.assertEqual(education.end_year, "")
        self.assertEqual(education.logo, "/static/img/UI.png")

    def test_required_fields_reject_invalid_input_without_writes(self):
        for field in ("school_name", "degree", "start_year"):
            for value in ("", "   ", None, "<b>", [], {}):
                with self.subTest(field=field, value=value):
                    serializer = EducationSerializer(data={**self.payload, field: value})
                    self.assertFalse(serializer.is_valid())
                    self.assertIn(field, serializer.errors)
            with self.subTest(field=field, omitted=True):
                payload = {key: value for key, value in self.payload.items() if key != field}
                serializer = EducationSerializer(data=payload)
                self.assertFalse(serializer.is_valid())
                self.assertIn(field, serializer.errors)
        self.assertEqual(Education.objects.count(), 1)

    def test_model_max_lengths_are_enforced(self):
        for field, length in (
            ("school_name", 255), ("degree", 255), ("start_year", 4),
            ("end_year", 4), ("logo", 255),
        ):
            with self.subTest(field=field):
                serializer = EducationSerializer(data={**self.payload, field: "x" * length})
                self.assertTrue(serializer.is_valid(), serializer.errors)
                serializer = EducationSerializer(data={**self.payload, field: "x" * (length + 1)})
                self.assertFalse(serializer.is_valid())
                self.assertIn(field, serializer.errors)
        self.assertEqual(Education.objects.count(), 1)

    def test_optional_fields_accept_omission_blank_and_null(self):
        serializer = EducationSerializer(data=self.payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        education = serializer.save()
        self.assertIsInstance(education.pk, uuid.UUID)
        self.assertEqual(str(education), "New School")
        self.assertIsNone(education.end_year)
        self.assertIsNone(education.logo)
        for value in ("", None):
            with self.subTest(value=value):
                serializer = EducationSerializer(education, data={
                    **self.payload, "end_year": value, "logo": value,
                })
                self.assertTrue(serializer.is_valid(), serializer.errors)
                serializer.save()
                education.refresh_from_db()
                self.assertEqual(education.end_year, value)
                self.assertEqual(education.logo, value)
                self.assertEqual(serializer.data["end_year"], value)
                self.assertEqual(serializer.data["logo"], value)

    def test_partial_update_preserves_identity_fields_and_stars(self):
        self.education.starred_by.add(self.visitor)
        original_pk = self.education.pk
        serializer = EducationSerializer(self.education, data={
            "school_name": "<b>Updated School</b>",
            "id": str(uuid.uuid4()), "star_count": 0, "is_starred": False,
            "starred_by": [],
        }, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.education.refresh_from_db()
        self.assertEqual(self.education.pk, original_pk)
        self.assertEqual(self.education.school_name, "Updated School")
        self.assertEqual(self.education.degree, "Information Systems")
        self.assertEqual(self.education.start_year, "2025")
        self.assertEqual(self.education.end_year, "2029")
        self.assertEqual(self.education.logo, "/static/img/UI.png")
        self.assertTrue(self.education.starred_by.filter(pk=self.visitor.pk).exists())
        self.assertEqual(Education.objects.count(), 1)


class EducationAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user("education-api-owner", is_superuser=True)
        self.visitor = User.objects.create_user("education-api-visitor")
        self.editor = User.objects.create_user("education-api-editor")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.staff = User.objects.create_user("education-api-staff", is_staff=True)
        self.education = Education.objects.create(
            school_name="Portfolio University", degree="Information Systems",
            start_year="2025", end_year="2029", logo="/static/img/UI.png",
        )
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.pk])
        self.star_url = reverse("api:education-star", args=[self.education.pk])
        self.payload = {
            "school_name": "New School", "degree": "Bachelor of Science",
            "start_year": "2026",
        }

    def test_public_list_and_detail(self):
        self.education.starred_by.add(self.visitor)
        for url in (self.list_url, self.detail_url):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
                data = response.data[0] if url == self.list_url else response.data
                self.assertEqual(data, {
                    "id": str(self.education.pk),
                    "school_name": "Portfolio University",
                    "degree": "Information Systems",
                    "start_year": "2025",
                    "end_year": "2029",
                    "logo": "/static/img/UI.png",
                    "star_count": 1,
                    "is_starred": False,
                })

    def test_search_ordering_and_empty_results(self):
        first = Education.objects.create(
            school_name="Alpha School", degree="Science", start_year="2020",
        )
        second = Education.objects.create(
            school_name="Alpha School", degree="Arts", start_year="2021",
        )
        expected = sorted((str(first.pk), str(second.pk))) + [str(self.education.pk)]
        for query in ({}, {"title": "   "}):
            response = self.client.get(self.list_url, query)
            self.assertEqual(response.status_code, 200)
            self.assertEqual([item["id"] for item in response.data], expected)
        response = self.client.get(self.list_url, {"title": "  PORTFOLIO  "})
        self.assertEqual([item["id"] for item in response.data], [str(self.education.pk)])
        self.assertEqual(self.client.get(self.list_url, {"title": "missing"}).data, [])

    def test_missing_records_and_permission_before_lookup(self):
        missing_detail = reverse("api:education-detail", args=[uuid.uuid4()])
        missing_star = reverse("api:education-star", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing_detail).status_code, 404)
        self.assertEqual(self.client.get("/api/v1/educations/invalid/").status_code, 404)
        self.client.force_authenticate(self.owner)
        for method, url, payload in (
            ("get", missing_detail, {}),
            ("put", missing_detail, self.payload),
            ("patch", missing_detail, {"degree": "Changed"}),
            ("delete", missing_detail, {}),
            ("post", missing_star, {}),
        ):
            with self.subTest(method=method):
                response = getattr(self.client, method)(url, payload, format="json")
                self.assertEqual(response.status_code, 404)
        self.client.force_authenticate(self.visitor)
        self.assertEqual(
            self.client.patch(missing_detail, {"degree": "Denied"}, format="json").status_code,
            403,
        )

    def test_guest_regular_and_staff_cannot_manage(self):
        self.education.starred_by.add(self.visitor)
        original = list(Education.objects.values())
        for user in (None, self.visitor, self.staff):
            self.client.force_authenticate(user=user)
            for method, url, payload in (
                ("post", self.list_url, self.payload),
                ("put", self.detail_url, self.payload),
                ("patch", self.detail_url, {"school_name": "Forbidden"}),
                ("delete", self.detail_url, {}),
            ):
                with self.subTest(user=user, method=method):
                    response = getattr(self.client, method)(url, payload, format="json")
                    self.assertEqual(response.status_code, 403)
                    self.assertEqual(list(Education.objects.values()), original)
                    self.assertEqual(
                        list(self.education.starred_by.values_list("pk", flat=True)),
                        [self.visitor.pk],
                    )

    def test_owner_can_create_and_sanitize_text(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "school_name": " <b>New School</b> ",
            "degree": "<i>Bachelor of Science</i>", "end_year": None,
            "logo": "<b>/static/img/UI.png</b>",
        }, format="json")
        self.assertEqual(response.status_code, 201)
        education = Education.objects.get(pk=response.data["id"])
        self.assertEqual(education.school_name, "New School")
        self.assertEqual(education.degree, "Bachelor of Science")
        self.assertEqual(education.logo, "/static/img/UI.png")
        self.assertIsNone(education.end_year)
        self.assertEqual(Education.objects.count(), 2)

    def test_owner_and_editor_updates_preserve_identity_and_stars(self):
        self.education.starred_by.add(self.visitor)
        original_pk = self.education.pk
        for user in (self.owner, self.editor):
            self.client.force_authenticate(user)
            response = self.client.patch(
                self.detail_url, {"school_name": "<b>Updated School</b>"}, format="json"
            )
            self.assertEqual(response.status_code, 200)
            self.education.refresh_from_db()
            self.assertEqual(self.education.school_name, "Updated School")
            self.assertEqual(self.education.degree, "Information Systems")
            self.assertEqual(self.education.end_year, "2029")
            self.assertEqual(self.education.logo, "/static/img/UI.png")
            for field in ("school_name", "degree", "start_year"):
                payload = {key: value for key, value in self.payload.items() if key != field}
                response = self.client.put(self.detail_url, payload, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)
            response = self.client.put(self.detail_url, {
                **self.payload, "end_year": None, "logo": "",
            }, format="json")
            self.assertEqual(response.status_code, 200)
            self.education.refresh_from_db()
            self.assertEqual(self.education.pk, original_pk)
            self.assertEqual(self.education.school_name, "New School")
            self.assertIsNone(self.education.end_year)
            self.assertEqual(self.education.logo, "")
            self.assertTrue(self.education.starred_by.filter(pk=self.visitor.pk).exists())
            self.assertEqual(Education.objects.count(), 1)
            self.education.degree = "Information Systems"
            self.education.end_year = "2029"
            self.education.logo = "/static/img/UI.png"
            self.education.save()

    def test_editor_cannot_create_or_delete(self):
        self.client.force_authenticate(self.editor)
        original = list(Education.objects.values())
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(list(Education.objects.values()), original)

    def test_invalid_input_is_rejected_without_writes(self):
        self.client.force_authenticate(self.owner)
        self.education.starred_by.add(self.visitor)
        original = list(Education.objects.values())
        for changes, field in (
            ({"school_name": "   "}, "school_name"),
            ({"school_name": "<b></b>"}, "school_name"),
            ({"degree": None}, "degree"),
            ({"degree": "<i></i>"}, "degree"),
            ({"school_name": "x" * 256}, "school_name"),
            ({"start_year": "<b>"}, "start_year"),
            ({"start_year": "20260"}, "start_year"),
            ({"end_year": "20290"}, "end_year"),
            ({"logo": "x" * 256}, "logo"),
        ):
            for method, url, payload in (
                ("post", self.list_url, {**self.payload, **changes}),
                ("put", self.detail_url, {**self.payload, **changes}),
                ("patch", self.detail_url, changes),
            ):
                with self.subTest(method=method, field=field, changes=changes):
                    response = getattr(self.client, method)(url, payload, format="json")
                    self.assertEqual(response.status_code, 400)
                    self.assertIn(field, response.data)
                    self.assertEqual(list(Education.objects.values()), original)
        response = self.client.post(self.list_url, '{"school_name":', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(list(Education.objects.values()), original)
        self.assertTrue(self.education.starred_by.filter(pk=self.visitor.pk).exists())

    def test_owner_can_delete(self):
        self.client.force_authenticate(self.owner)
        self.education.starred_by.add(self.visitor)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Education.objects.filter(pk=self.education.pk).exists())

    def test_star_requires_login_and_preserves_other_users(self):
        self.education.starred_by.add(self.visitor)
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assertEqual(self.client.get(self.star_url).status_code, 403)
        for user in (self.staff, self.editor, self.owner):
            self.client.force_authenticate(user)
            for expected, count in ((True, 2), (False, 1)):
                with self.subTest(user=user, expected=expected):
                    response = self.client.post(
                        self.star_url, {"user_id": self.visitor.pk}, format="json"
                    )
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.data["is_starred"], expected)
                    self.assertEqual(response.data["star_count"], count)
                    self.assertEqual(self.education.starred_by.filter(pk=user.pk).exists(), expected)
                    self.assertTrue(self.education.starred_by.filter(pk=self.visitor.pk).exists())
        self.client.force_authenticate(self.visitor)
        for expected, count in ((False, 0), (True, 1)):
            response = self.client.post(self.star_url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data["is_starred"], expected)
            self.assertEqual(response.data["star_count"], count)

    def test_identity_and_star_fields_are_read_only(self):
        self.client.force_authenticate(self.owner)
        forged_id = uuid.uuid4()
        forged = {
            "id": str(forged_id), "star_count": 99, "is_starred": True,
            "starred_by": [self.staff.pk],
        }
        response = self.client.post(self.list_url, {**self.payload, **forged}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], str(forged_id))
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(Education.objects.get(pk=response.data["id"]).starred_by.count(), 0)
        self.education.starred_by.add(self.visitor)
        response = self.client.patch(self.detail_url, forged, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.education.pk))
        self.assertEqual(response.data["star_count"], 1)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(
            list(self.education.starred_by.values_list("pk", flat=True)), [self.visitor.pk]
        )

    def test_unsupported_and_safe_methods(self):
        self.client.force_authenticate(self.owner)
        original = list(Education.objects.values())
        for url, method in (
            (self.list_url, "put"), (self.list_url, "patch"), (self.list_url, "delete"),
            (self.detail_url, "post"), (self.star_url, "get"),
            (self.star_url, "put"), (self.star_url, "patch"), (self.star_url, "delete"),
        ):
            with self.subTest(url=url, method=method):
                self.assertEqual(getattr(self.client, method)(url).status_code, 405)
        self.client.force_authenticate(user=None)
        for url in (self.list_url, self.detail_url):
            self.assertEqual(self.client.head(url).status_code, 200)
            self.assertEqual(self.client.options(url).status_code, 200)
        self.assertEqual(list(Education.objects.values()), original)
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_session_csrf_is_enforced_for_mutations(self):
        client = APIClient(enforce_csrf_checks=True)
        self.owner.set_password("education-api-csrf-password")
        self.owner.save(update_fields=["password"])
        self.assertTrue(client.login(
            username=self.owner.username, password="education-api-csrf-password"
        ))
        original = list(Education.objects.values())
        mutations = (
            ("post", self.list_url, self.payload),
            ("put", self.detail_url, self.payload),
            ("patch", self.detail_url, {"degree": "Changed"}),
            ("delete", self.detail_url, {}),
            ("post", self.star_url, {}),
        )
        for method, url, payload in mutations:
            with self.subTest(method=method, token="missing"):
                response = getattr(client, method)(url, payload, format="json")
                self.assertEqual(response.status_code, 403)
        self.assertEqual(list(Education.objects.values()), original)
        self.assertEqual(self.education.starred_by.count(), 0)
        client.get(reverse("main:show_education"))
        self.assertIn("csrftoken", client.cookies)
        for method, url, payload in mutations:
            with self.subTest(method=method, token="invalid"):
                response = getattr(client, method)(
                    url, payload, format="json", HTTP_X_CSRFTOKEN="invalid"
                )
                self.assertEqual(response.status_code, 403)
        self.assertEqual(list(Education.objects.values()), original)
        self.assertEqual(self.education.starred_by.count(), 0)
        headers = {"HTTP_X_CSRFTOKEN": client.cookies["csrftoken"].value}
        self.assertEqual(client.post(self.list_url, self.payload, format="json", **headers).status_code, 201)
        self.assertEqual(client.put(self.detail_url, self.payload, format="json", **headers).status_code, 200)
        self.assertEqual(client.patch(
            self.detail_url, {"degree": "Session update"}, format="json", **headers
        ).status_code, 200)
        response = client.post(self.star_url, format="json", **headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        deleted = client.delete(self.detail_url, **headers)
        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(deleted.content, b"")

    def test_list_queries_do_not_grow_per_record(self):
        for index in range(5):
            education = Education.objects.create(
                school_name=f"School {index}", degree="Science", start_year="2025",
            )
            education.starred_by.add(self.visitor)
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            with self.subTest(user=user):
                with self.assertNumQueries(2):
                    response = self.client.get(self.list_url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.data), 6)


class EducationPageIntegrationTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user("education-page-owner", is_superuser=True)
        self.editor = User.objects.create_user("education-page-editor")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.visitor = User.objects.create_user("education-page-visitor")
        self.staff = User.objects.create_user("education-page-staff", is_staff=True)
        self.education = Education.objects.create(
            school_name="Original School", degree="Science", start_year="2025",
        )
        self.page_url = reverse("main:show_education")
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.pk])
        self.star_url = reverse("api:education-star", args=[self.education.pk])
        self.payload = {
            "school_name": "New School", "degree": "Arts", "start_year": "2026",
        }

    def test_page_api_configuration_controls_and_csrf_for_all_roles(self):
        for user in (None, self.visitor, self.staff, self.editor, self.owner):
            with self.subTest(user=user):
                client = APIClient(enforce_csrf_checks=True)
                if user:
                    client.force_login(user)
                response = client.get(self.page_url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, "education.html")
                self.assertIn("csrftoken", client.cookies)
                self.assertContains(response, f'const BASE_EDUCATIONS_ENDPOINT = "{self.list_url}";')
                self.assertContains(response, 'const DETAIL_EDUCATION_ENDPOINT = "/api/v1/educations/')
                self.assertContains(response, 'const STAR_EDUCATION_ENDPOINT = "/api/v1/educations/')
                self.assertNotContains(response, reverse("main:get_educations_json"))
                self.assertNotContains(response, reverse("main:create_education_ajax"))
                self.assertNotContains(response, "item.fields")
                self.assertNotContains(response, "item.pk")
                self.assertNotContains(response, "localStorage")
                authenticated = "true" if user else "false"
                self.assertContains(
                    response, f'const IS_AUTHENTICATED = "{authenticated}" === "true";'
                )
                if user == self.owner:
                    self.assertContains(response, 'id="add-education-modal"')
                else:
                    self.assertNotContains(response, 'id="add-education-modal"')
                if user in (self.owner, self.editor):
                    self.assertContains(response, 'id="edit-education-modal"')
                    self.assertContains(response, 'id="edit_school_name"')
                    self.assertEqual(response.context["edit_form"].auto_id, "edit_%s")
                else:
                    self.assertNotContains(response, 'id="edit-education-modal"')
                headers = {"HTTP_X_CSRFTOKEN": client.cookies["csrftoken"].value}
                self.assertEqual(client.get(self.list_url).status_code, 200)
                star = client.post(self.star_url, format="json", **headers)
                self.assertEqual(star.status_code, 200 if user else 403)
                updated = client.patch(
                    self.detail_url, {"degree": "Changed"}, format="json", **headers
                )
                self.assertEqual(
                    updated.status_code, 200 if user in (self.owner, self.editor) else 403
                )
                created = client.post(self.list_url, self.payload, format="json", **headers)
                self.assertEqual(created.status_code, 201 if user == self.owner else 403)
                deleted = client.delete(self.detail_url, **headers)
                self.assertEqual(deleted.status_code, 204 if user == self.owner else 403)

    def test_page_supports_ajax_edit_errors_and_safe_rendering(self):
        self.client.force_login(self.owner)
        response = self.client.get(self.page_url)
        for fragment in (
            "event.preventDefault()", "isEdit ? 'PATCH' : 'POST'",
            "'X-CSRFToken'", "credentials: 'same-origin'",
            "escapeHtml(education.school_name)", "escapeHtml(education.degree)",
            "escapeHtml(education.star_count)", "escapeHtml(logo)",
            "window.confirm(", "data.is_starred", "new AbortController()",
            "showToast('Gagal menyimpan education', error.message, 'error')",
        ):
            self.assertContains(response, fragment)
        self.assertEqual(
            response.context["form"]["school_name"].id_for_label, "id_school_name"
        )

    def test_page_cookie_supports_real_session_csrf(self):
        self.owner.set_password("education-page-session-password")
        self.owner.save(update_fields=["password"])
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(
            username=self.owner.username, password="education-page-session-password"
        ))
        response = client.get(self.page_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("csrftoken", client.cookies)
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        headers = {"HTTP_X_CSRFTOKEN": client.cookies["csrftoken"].value}
        created = client.post(self.list_url, self.payload, format="json", **headers)
        self.assertEqual(created.status_code, 201)
        updated = client.patch(
            self.detail_url, {"logo": None, "end_year": ""}, format="json", **headers
        )
        self.assertEqual(updated.status_code, 200)
        self.assertIsNone(updated.data["logo"])
        self.assertEqual(updated.data["end_year"], "")

    def test_dialog_accessibility_and_keyboard_support(self):
        for user in (self.owner, self.editor):
            with self.subTest(user=user):
                self.client.force_login(user)
                response = self.client.get(self.page_url)
                self.assertContains(response, 'aria-labelledby="edit-education-title"')
                self.assertContains(response, 'id="edit-education-title"')
                if user == self.owner:
                    self.assertContains(response, 'aria-labelledby="add-education-title"')
                    self.assertContains(response, 'id="add-education-title"')
                for fragment in (
                    'aria-label="Tutup"', 'tabindex="-1"',
                    "modal.addEventListener('keydown'",
                    "event.key !== 'Tab'", "section.inert = open",
                    'modal.querySelector(\'[name="school_name"]\').focus()',
                    "modal.educationTrigger", "trigger.isConnected",
                ):
                    self.assertContains(response, fragment)

    def test_status_announcements_and_broken_logo_handling(self):
        response = self.client.get(self.page_url)
        for fragment in (
            "document.body.classList.add('education-page')",
            "image.addEventListener('error', () => image.remove())",
            "toast.setAttribute('role', 'status')",
            "toast.setAttribute('aria-live', 'polite')",
            "loadingState.setAttribute('role', 'status')",
            "errorState.setAttribute('role', 'alert')",
            "emptyState.setAttribute('role', 'status')",
        ):
            self.assertContains(response, fragment)

    def test_legacy_education_routes_preserve_role_boundaries(self):
        create_url = reverse("main:create_education")
        ajax_url = reverse("main:create_education_ajax")
        update_url = reverse("main:update_education", args=[self.education.pk])
        delete_url = reverse("main:delete_education", args=[self.education.pk])
        for user in (None, self.visitor, self.staff, self.editor):
            with self.subTest(user=user):
                client = APIClient()
                if user:
                    client.force_login(user)
                for method in ("get", "post"):
                    response = getattr(client, method)(create_url, self.payload)
                    self.assertEqual(response.status_code, 403 if user else 302)
                self.assertEqual(client.post(ajax_url, self.payload).status_code, 403)
                self.assertEqual(client.post(delete_url).status_code, 403 if user else 302)
                for method in ("get", "post"):
                    response = getattr(client, method)(update_url, self.payload)
                    expected = 302 if not user or (user == self.editor and method == "post") else 403
                    if user == self.editor and method == "get":
                        expected = 200
                    self.assertEqual(response.status_code, expected)
                self.assertEqual(Education.objects.count(), 1)
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(create_url).status_code, 200)
        self.assertEqual(self.client.get(update_url).status_code, 200)
        self.assertEqual(self.client.get(delete_url).status_code, 405)
        data = self.client.get(reverse("main:get_educations_json")).json()
        self.assertEqual(data[0]["pk"], str(self.education.pk))
