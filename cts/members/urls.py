from django.conf.urls import url
from django.views.generic import TemplateView

from .views import (
    CorporateMemberRenewView, CorporateMemberSignUpView,
    IndividualMemberListView, TeamsListView, corporate_member_list_view, about_corp_membership
)

app_name = 'members'
urlpatterns = [
    url(r'^individual-members/$', IndividualMemberListView.as_view(), name='individual-members'),
    url(r'^corporate-members/$', corporate_member_list_view, name='corporate-members'),
    url(r'^corporate-membership/$', about_corp_membership, name='about-corporate-membership'),
    url(r'^corporate-membership/join/$', CorporateMemberSignUpView.as_view(), name='corporate-members-join'),
    url(
        r'^corporate-membership/renew/(?P<token>[A-Za-z0-9:_-]+)/$',
        CorporateMemberRenewView.as_view(),
        name='corporate-members-renew',
    ),
    url(
        r'^corporate-membership/join/thanks/$',
        TemplateView.as_view(template_name='members/corporate_members_join_thanks.html'),
        name='corporate-members-join-thanks',
    ),
    url('^teams/$', TeamsListView.as_view(), name='teams'),
]
