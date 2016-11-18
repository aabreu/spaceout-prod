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

from spaceoutvr.serializers import SpaceoutUserSerializer, SpaceoutRoomSerializer, SpaceoutCommentSerializer, SpaceoutContentSerializer
from spaceoutvr.models import SpaceoutUser, SpaceoutRoom, SpaceoutContent, SpaceoutRoomDefinition, SpaceoutComment
from spaceoutvr.storage import IBMObjectStorage

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
        try:
            user = SpaceoutUser.objects.get(id=request.data['user_id'])
            room = user.spaceoutroom_set.first()
            if room == None:
                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(SpaceoutRoomSerializer(room).data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        user = request.user

        # create the first room, if room is empty
        if user.spaceoutroom_set.count() == 0:
            roomDefinition = SpaceoutRoomDefinition.objects.get(
                type=SpaceoutRoomDefinition.ROOM_TYPE_HOME
            )
            room = SpaceoutRoom(user_id=user.id)
            room.definition = roomDefinition
            room.save()

        room = user.spaceoutroom_set.first()
        content = request.data['spaceoutcontent_set']
        # room.spaceoutcontent_set.all().delete()
        for c in content:
            # try to get a content room by ids
            try:
                contentModel = SpaceoutContent.objects.get(
                    room_id = room.id,
                    idx = c['idx'],
                )
            except:
                contentModel = SpaceoutContent(room_id=room.id)
                room.spaceoutcontent_set.add(contentModel)

            contentModel.url = c['url']
            contentModel.type = c['type']
            contentModel.source = c['source']
            contentModel.query = c['query']
            contentModel.weight = c['weight']
            contentModel.idx = c['idx']
            contentModel.save()

        room.save()
        return Response(SpaceoutRoomSerializer(room).data)

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

class ContentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        c = request.data
        content = SpaceoutContent.objects.get(id=c['id'])
        if user.id == content.room.user.id:
            content.url = c['url']
            content.type = c['type']
            content.source = c['source']
            content.query = c['query']
            content.weight = c['weight']
            content.idx = c['idx']
            content.save()
            return Response(SpaceoutContentSerializer(content).data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

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
            if key == 'notifications_id':
                user.notification_id = request.data['notifications_id']
            if key == 'latitude':
                user.latitude = request.data['latitude']
            if key == 'longitude':
                user.longitude = request.data['longitude']
            if key == 'personality_insights':
                user.personality_insights = request.data['personality_insights']
            if key == 'first_name':
                user.first_name = request.data['first_name']
            if key == 'last_name':
                user.last_name = request.data['last_name']

        user.save()

        return Response(status=status.HTTP_200_OK)

class CommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        author = request.user
        # author = SpaceoutUser.objects.get(id=1)
        content = SpaceoutContent.objects.get(id=request.data['content_id'])
        comment = SpaceoutComment(
            author=author,
            content=content,
            audio_file=request.FILES['file'],
        )
        comment.save()
        return Response(SpaceoutCommentSerializer(comment).data)

    def delete(self, request, format=None):
        author = request.user
        comment = SpaceoutComment.objects.get(id=request.data['comment_id'])
        if author.id != comment.author.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        room_id = comment.content.room.id
        content_id = comment.content.id
        comment_id = comment.id

        # delete model
        comment.delete()

        return Response({
            'comment_id':comment_id,
            'content_id':content_id,
            'room_id':room_id,
        })

class DebugView(APIView):
    def get(self, request, format=None):
        user = SpaceoutUser.objects.get(id=6)
        room = user.spaceoutroom_set.first()

        if room == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(SpaceoutRoomSerializer(room).data)
        # user = SpaceoutUser.objects.all()
        # return Response(SpaceoutUserSerializer(user, many=True).data)

        # rooms = SpaceoutRoom.objects.all()
        # return Response(SpaceoutRoomSerializer(rooms, many=True).data)

        # storage = IBMObjectStorage()
        # storage.exists("lalala")
        # return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        author = SpaceoutUser.objects.get(id=1)
        content = SpaceoutContent.objects.get(id=1)
        comment = SpaceoutComment(
            author=author,
            content=content,
            audio_file=request.FILES['file'],
        )
        comment.save()
        return Response(SpaceoutCommentSerializer(comment).data)

        # storage = IBMObjectStorage()
        # storage.get_token()
        # return Response(status=status.HTTP_200_OK)

        # users = SpaceoutUser.objects.all()
        # return Response(SpaceoutUserSerializer(users, many=True).data)

        # rooms = SpaceoutRoom.objects.all()
        # return Response(SpaceoutRoomSerializer(rooms, many=True).data)

        # user = SpaceoutUser.objects.get(id=3)
        # room = user.spaceoutroom_set.first()
        # if room == None:
        #     return Response({'error':'si'})
        # else:
        #     return Response(SpaceoutRoomSerializer(room).data)
