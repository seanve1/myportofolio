from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Organization
from main.permissions import IsPortfolioOwnerOrEditorOrReadOnly
from main.serializers import OrganizationSerializer


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def organization_list(request):
    if request.method in ("GET", "HEAD"):
        organizations = Organization.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            organizations = organizations.filter(title__icontains=title)
        serializer = OrganizationSerializer(organizations, many=True, context={"request": request})
        return Response(serializer.data)

    serializer = OrganizationSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def organization_detail(request, organization_id):
    organization = get_object_or_404(
        Organization.objects.prefetch_related("starred_by"), pk=organization_id,
    )
    if request.method in ("GET", "HEAD"):
        return Response(OrganizationSerializer(organization, context={"request": request}).data)
    if request.method == "DELETE":
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = OrganizationSerializer(
        organization, data=request.data, partial=request.method == "PATCH",
        context={"request": request},
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def organization_star(request, organization_id):
    organization = get_object_or_404(Organization, pk=organization_id)
    if organization.starred_by.filter(pk=request.user.pk).exists():
        organization.starred_by.remove(request.user)
    else:
        organization.starred_by.add(request.user)
    return Response(OrganizationSerializer(organization, context={"request": request}).data)
