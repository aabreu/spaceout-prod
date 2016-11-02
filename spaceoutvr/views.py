from django.conf import settings
from django.core.urlresolvers import reverse
from django.core import serializers
from django.forms.utils import ErrorList
from django.forms.forms import NON_FIELD_ERRORS
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.views.generic.edit import FormView

from authemail import wrapper

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import SignupForm, LoginForm, PasswordResetForm
from .forms import PasswordResetVerifiedForm, PasswordChangeForm

from spaceoutvr.serializers import SpaceoutUserSerializer, SpaceoutRoomSerializer
from spaceoutvr.models import SpaceoutUser, SpaceoutRoom, SpaceoutContent


import hashlib

class LandingView(TemplateView):
    template_name = 'landing.html'


class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm

    def form_valid(self, form):
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        account = wrapper.Authemail()
        account.base_uri = "%s/api" % settings.SERVER_URL
        response = account.signup(first_name=first_name, last_name=last_name,
            email=email, password=password)

        # Handle other error responses from API
        if 'detail' in response:
            form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(SignupView, self).form_valid(form)

    def get_success_url(self):
        return reverse('signup_email_sent_page')


class SignupEmailSentView(TemplateView):
    template_name = 'signup_email_sent.html'


class SignupVerifyView(View):
    def get(self, request, format=None):
        code = request.GET.get('code', '')

        account = wrapper.Authemail()
        account.base_uri = "%s/api" % settings.SERVER_URL

        response = account.signup_verify(code=code)

        # Handle other error responses from API
        if 'detail' in response:
            return HttpResponseRedirect(reverse('signup_not_verified_page'))

        return HttpResponseRedirect(reverse('signup_verified_page'))


class SignupVerifiedView(TemplateView):
    template_name = 'signup_verified.html'


class SignupNotVerifiedView(TemplateView):
    template_name = 'signup_not_verified.html'


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        account = wrapper.Authemail()
        account.base_uri = "%s/api" % settings.SERVER_URL
        response = account.login(email=email, password=password)

        if 'token' in response:
            self.request.session['auth_token'] = response['token']
        else:
            # Handle other error responses from API
            if 'detail' in response:
                form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse('home_page')


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        token = self.request.session['auth_token']

        account = wrapper.Authemail()
        account.base_uri = "%s/api" % settings.SERVER_URL
        response = account.users_me(token=token)

        context['email'] = response['email']

        return context


class LogoutView(View):
    def get(self, request):
        token = self.request.session['auth_token']

        account = wrapper.Authemail()
        account.base_uri = "%s/api" % settings.SERVER_URL
        response = account.logout(token=token)

        self.request.session.flush()

        return HttpResponseRedirect(reverse('landing_page'))


class PasswordResetView(FormView):
    template_name = 'password_reset.html'
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']

        account = wrapper.Authemail()
        account.base_uri = "%s/api" % settings.SERVER_URL
        response = account.password_reset(email=email)

        # Handle other error responses from API
        if 'detail' in response:
            form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(PasswordResetView, self).form_valid(form)

    def get_success_url(self):
        return reverse('password_reset_email_sent_page')


class PasswordResetEmailSentView(TemplateView):
    template_name = 'password_reset_email_sent.html'


class PasswordResetVerifyView(View):
    def get(self, request, format=None):
        code = request.GET.get('code', '')

        account = wrapper.Authemail()
        account.base_uri = "%s/api" % settings.SERVER_URL
        response = account.password_reset_verify(code=code)

        # Handle other error responses from API
        if 'detail' in response:
            return HttpResponseRedirect(
                reverse('password_reset_not_verified_page'))

        request.session['password_reset_code'] = code

        return HttpResponseRedirect(reverse('password_reset_verified_page'))


class PasswordResetVerifiedView(FormView):
    template_name = 'password_reset_verified.html'
    form_class = PasswordResetVerifiedForm

    def form_valid(self, form):
        code = self.request.session['password_reset_code']
        password = form.cleaned_data['password']

        m = hashlib.md5()
        m.update(password.encode('utf-8'))
        encryptedPassword = m.hexdigest()

        account = wrapper.Authemail()
        account.base_uri = "%s/api" % settings.SERVER_URL
        response = account.password_reset_verified(code=code, password=encryptedPassword)

        # Handle other error responses from API
        if 'detail' in response:
            form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(PasswordResetVerifiedView, self).form_valid(form)

    def get_success_url(self):
        return reverse('password_reset_success')


class PasswordResetNotVerifiedView(TemplateView):
    template_name = 'password_reset_not_verified.html'


class PasswordResetSuccessView(TemplateView):
    template_name = 'password_reset_success.html'


class PasswordChangeView(FormView):
    template_name = 'password_change.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        token = self.request.session['auth_token']
        password = form.cleaned_data['password']

        account = wrapper.Authemail()
        account.base_uri = "%s/api" % settings.SERVER_URL
        response = account.password_change(token=token, password=password)

        # Handle other error responses from API
        if 'detail' in response:
            form.add_error(None, response['detail'])
            return self.form_invalid(form)

        return super(PasswordChangeView, self).form_valid(form)

    def get_success_url(self):
        return reverse('home_page')

class RoomView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        for key in request.data:
            if key == 'user_id':
                user = SpaceoutUser.objects.get(id=request.data['user_id'])
                room = user.spaceoutroom_set.first()
                if room == None:
                    return Response()
                else:
                    return Response(SpaceoutRoomSerializer(room).data)

        return Response(status=status.HTTP_404)

    def post(self, request, format=None):
        user = request.user
        if user.spaceoutroom_set.count() == 0:
            room = SpaceoutRoom(user_id=user.id)
            room.type = SpaceoutRoom.ROOM_TYPE_HOME
            # user.spaceoutroom_set.add(room)
            # user.save()
            room.save()

        room = user.spaceoutroom_set.all()[0]
        for key in request.data:
            if key == 'spaceoutcontent_set':
                content = request.data['spaceoutcontent_set']
                room.spaceoutcontent_set.all().delete()
                for c in content:
                    contentModel = SpaceoutContent(room_id=room.id)
                    contentModel.url = c['url']
                    contentModel.type = c['type']
                    contentModel.source = c['source']
                    contentModel.query = c['query']
                    contentModel.idx = c['idx']
                    contentModel.save()

                    room.spaceoutcontent_set.add(contentModel)

        room.save()
        return Response(status=status.HTTP_200_OK)

class FriendsView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):

        for key in request.data:
            if key == 'ids':
                ids = request.data['ids']
            if key == 'social':
                social = request.data['social']

        friends = SpaceoutUser.objects.all().filter(facebook_id__in=ids)
        return Response(SpaceoutUserSerializer(friends, many=True).data)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SpaceoutUserSerializer

    def get(self, request, format=None):
        return Response(self.serializer_class(request.user).data)

    def post(self, request, format=None):
        user = request.user

        for key in request.data:
            if key == 'facebook_id':
                user.facebook_id = request.data['facebook_id']
            if key == 'reddit_id':
                user.reddit_id = request.data['reddit_id']
            if key == 'soundcloud_id':
                user.soundcloud_id = request.data['soundcloud_id']
            if key == 'soundcloud_id':
                user.twitter_id = request.data['twitter_id']
            if key == 'notification_id':
                user.notification_id = request.data['notification_id']
            if key == 'latitude':
                user.notification_id = request.data['latitude']
            if key == 'longitude':
                user.notification_id = request.data['longitude']

        user.save()

        return Response()


class DebugView(APIView):
    def get(self, request, format=None):
        # users = SpaceoutUser.objects.all()
        # return Response(SpaceoutUserSerializer(users, many=True).data)

        # rooms = SpaceoutRoom.objects.all()
        # return Response(SpaceoutRoomSerializer(rooms, many=True).data)

        user = SpaceoutUser.objects.get(id=3)
        room = user.spaceoutroom_set.first()
        if room == None:
            return Response({'error':'si'})
        else:
            return Response(SpaceoutRoomSerializer(room).data)
