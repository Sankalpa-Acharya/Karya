from email import message
from http.client import HTTPResponse
from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.views import View
from .models import *
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class HomePageView(TemplateView):
    template_name = 'work/home.html'


class SingupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/projects')
        fm = SingupForm()
        context = {'form': fm}
        return render(request, 'work/singup.html', context)

    def post(self, request):
        fm = SingupForm(request.POST)
        if fm.is_valid():
            fm.save()
        context = {'form': fm}
        return render(request, 'work/singup.html', context)


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/projects')
        fm = AuthenticationForm()
        context = {'form': fm}
        return render(request, 'work/login.html', context)

    def post(self, request):
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = request.POST['username']
            upass = request.POST['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/projects')
        context = {'form': fm}
        return render(request, 'work/login.html', context)


class ProjectView(View):

    @method_decorator(login_required(login_url='/account/login'))
    def get(self, request):
        user_projects = Project.objects.filter(
            user__username=request.user.username)
        context = {'project': user_projects, 'status': 'undone'}
        return render(request, 'work/project.html', context)


class DashboardView(View):

    @method_decorator(login_required(login_url='/account/login'))
    def get(self, request, pid, status):
        try:
            user_project = Project.objects.get(id=pid, user=request.user)
            card = Card.objects.filter(project=user_project, status=status)
            context = {
                'project_id': pid,
                'cards': card,
                'username': request.user.username,
                'profile_pic': request.user.profile_pic}
            return render(request, 'work/dashboard.html', context)
        except BaseException:
            return HttpResponseRedirect('/404')


class MembersView(View):

    @method_decorator(login_required(login_url='/account/login'))
    def get(self, request, pid):
        try:
            project_members = Project.objects.get(id=pid)
            project_members = project_members.user.all()
            context = {
                'members': project_members,
                'project_id': pid,
                'username': request.user.username,
                'profile_pic': request.user.profile_pic}
            return render(request, 'work/members.html', context)
        except BaseException:
            return HttpResponseRedirect('/404')


class ProfileEditView(View):

    @method_decorator(login_required(login_url='/account/login'))
    def get(self, request, pid):
        fm = ProfileEditForm(instance=request.user)
        context = {
            'form': fm,
            'user': request.user,
            'profile_pic': request.user.profile_pic,
            'project_id': pid}
        return render(request, 'work/profile_edit.html', context)

    @method_decorator(login_required(login_url='/account/login'))
    def post(self, request, pid):
        fm = ProfileEditForm(request.POST, instance=request.user)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Profile is Updated')
        context = {'form': fm,
                   'profile_pic': request.user.profile_pic, 'project_id': pid}
        return render(request, 'work/profile_edit.html', context)


@login_required(login_url='/account/login')
def profile_pic_change(request, pid):
    if request.method == 'POST':
        fm = ProfilePictureChangeForm(
            request.POST, request.FILES, instance=request.user)
        if fm.is_valid():
            fm.save()
            messages.success(request, 'Profile Picture is Updated')
            return HttpResponseRedirect(f'/edit/{pid}')
    return HttpResponseRedirect(f'/edit/{pid}')


class CardView(View):

    @method_decorator(login_required(login_url='/account/login'))
    def get(self, request, pid, cardtitle):
        fm = CardStatusChangeForm()
        card = Card.objects.get(project__id=pid, slug=cardtitle)
        card_timeline = History.objects.filter(card=card)
        context = {
            'profile_pic': request.user.profile_pic,
            'card': card,
            'form': fm,
            'project_id': pid,
            'card_timeline': card_timeline}
        return render(request, 'work/card_view.html', context)

    @method_decorator(login_required(login_url='/account/login'))
    def post(self, request, pid, cardtitle):
        card = Card.objects.get(project__id=pid, slug=cardtitle)
        fm = CardStatusChangeForm(request.POST, instance=card)
        card_timeline = History.objects.filter(card=card)
        if fm.is_valid():
            History.objects.create(
                card=card,
                user=request.user,
                status=request.POST['status'])
            fm.save()
            messages.success(request, 'card is updated')
        context = {
            'profile_pic': request.user.profile_pic,
            'card': card,
            'form': fm,
            'project_id': pid,
            'card_timeline': card_timeline}
        return render(request, 'work/card_view.html', context)


class AddCardView(View):
    @method_decorator(login_required(login_url='/account/login'))
    def get(self, request, pid):
        fm = AddCardForm()
        context = {'form': fm, 'project_id': pid,
                   'profile_pic': request.user.profile_pic}
        return render(request, 'work/add_card.html', context)

    @method_decorator(login_required(login_url='/account/login'))
    def post(self, request, pid):
        fm = AddCardForm(request.POST)
        card_title = request.POST['title']
        card = Card.objects.filter(project__id=pid, title=card_title)
        if len(card) > 0:
            messages.warning(request, 'Card with this title already exsist')
        else:
            if fm.is_valid():
                card = fm.save(commit=False)
                card.project = Project.objects.get(id=pid)
                card.save()
                History.objects.create(card=card, user=request.user)
                messages.success(request, 'Card is Added')
                return HttpResponseRedirect(f'/dashboard/{pid}/undone')
        context = {'form': fm, 'project_id': pid,
                   'profile_pic': request.user.profile_pic}
        return render(request, 'work/add_card.html', context)


class CreateProjectView(View):

    @method_decorator(login_required(login_url='/account/login'))
    def get(self, request):
        fm = AddProjectForm()
        context = {'form': fm}
        return render(request, 'work/create_project.html', context)

    @method_decorator(login_required(login_url='/account/login'))
    def post(self, request):
        fm = AddProjectForm(request.POST)
        if fm.is_valid():
            project = fm.save(commit=False)
            project.save()
            project.user.add(request.user)
            messages.success(request, 'Project has been created')
            return HttpResponseRedirect('/projects')


class InviteView(View):

    @method_decorator(login_required(login_url='/account/login'))
    def get(self, request, pid):
        project = Project.objects.get(id=pid)
        try:
            if len(Link) > 0:
                Link = Link[0]
        except:
            Link = InviteLink.objects.create(
                project=project, user=request.user)
        context = {
            'Invite_Link': Link,
            'project_id': pid,
            'profile_pic': request.user.profile_pic,
            'request': request}
        return render(request, 'work/invite.html', context)


class InviteAccept(View):

    @method_decorator(login_required(login_url='/account/login'))
    def get(self, request, pid):
        try:
            link = InviteLink.objects.get(id=pid)
            project = link.project
            project.user.add(request.user)
            messages.success(request, 'New Project Added')
            link.delete()
            return HttpResponseRedirect(f'/dashboard/{project.id}/undone')
        except BaseException:
            return render(
                request,
                '404.html',
                {
                    'message': 'Broken Link',
                    'message_description': 'This is link is broken, please ask for another'})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def error(request):
    return render(request, '404.html')
