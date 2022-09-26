from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.HomePageView.as_view(), name='home'),
    path("account/login", views.LoginView.as_view(), name='login'),
    path("account/singup", views.SingupView.as_view(), name='singup'),
    path("projects/", views.ProjectView.as_view(), name='projects'),
    path("createp/", views.CreateProjectView.as_view(), name='create_project'),
    path("dashboard/<str:pid>/members", views.MembersView.as_view(), name='members'),
    path("dashboard/<str:pid>/<str:status>", views.DashboardView.as_view(), name='dashboard'),
    path("edit/<str:pid>", views.ProfileEditView.as_view(), name='edit_profile'),
    path("picchange/<str:pid>", views.profile_pic_change, name='picchange'),
    path('card/<str:pid>/<slug:cardtitle>', views.CardView.as_view(), name='cardview'),
    path("addcard/<str:pid>/", views.AddCardView.as_view(), name='addcard'),
    path('invite/<str:pid>', views.InviteView.as_view(), name='invite'),
    path('invite_accept/<str:pid>', views.InviteAccept.as_view(), name='inviteaccept'),
    path("404/", views.error, name='home'),
    path("logout/", views.logout_view, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
