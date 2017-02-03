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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.core.exceptions import MultipleObjectsReturned

from authemail import wrapper
from authemail.models import SignupCode

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PaginationSerializer

from .forms import SignupForm, LoginForm, PasswordResetForm
from .forms import PasswordResetVerifiedForm, PasswordChangeForm

from spaceoutvr.serializers import SpaceoutUserSerializer, SpaceoutRoomSerializer
from spaceoutvr.serializers import SpaceoutCommentSerializer, SpaceoutContentSerializer, SpaceoutNotificationSerializer
from spaceoutvr.serializers import SpaceoutUserNotificationsSerializer, SpaceoutUserSimpleSerializer
from spaceoutvr.serializers import WatsonBlacklistSerializer, PeopleSeriaizer
from spaceoutvr.models import SpaceoutUser, SpaceoutRoom, SpaceoutContent, SpaceoutRoomDefinition, SpaceoutComment, SpaceoutNotification
from spaceoutvr.models import WatsonInput, WatsonOutput, WatsonBlacklist, personality_insights_output_directory_path, featured_directory_path
from spaceoutvr.notifications import OneSignalNotifications
from spaceoutvr.storage import WatsonStorage, MiscStorage
from spaceoutvr.facebook import FacebookBackend

from datetime import datetime

import hashlib
import hmac
import json
import requests

class LandingView(TemplateView):
    template_name = 'landing.html'

def users_with_room():
    return SpaceoutUser.objects.annotate(count=Count('spaceoutroom__spaceoutcontent')).filter(count__gt = 0)

def send_signup_email(user, request):
    # send validation email
    ipaddr = request.META.get('REMOTE_ADDR', '0.0.0.0')
    signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
    signup_code.send_signup_email()

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
            user = SpaceoutUser.objects.get(id=request.query_params['user_id'])
            room = user.spaceoutroom_set.first()
            if room == None:
                roomDefinition = SpaceoutRoomDefinition.objects.get(
                    type=SpaceoutRoomDefinition.ROOM_TYPE_HOME
                )
                room = SpaceoutRoom(user_id=user.id)
                room.definition = roomDefinition
                room.save()

            return Response(SpaceoutRoomSerializer(room).data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        user = request.user
        user.last_activity = datetime.now()
        user.save()

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
            add_to_collection = False
            try:
                contentModel = SpaceoutContent.objects.get(
                    room_id = room.id,
                    idx = c['idx'],
                )
            except:
                contentModel = SpaceoutContent(room_id=room.id)
                add_to_collection = True

            contentModel.url = c['url']
            contentModel.type = c['type']
            contentModel.source = c['source']
            contentModel.query = c['query']
            contentModel.weight = c['weight']
            contentModel.idx = c['idx']
            contentModel.save()

            if(add_to_collection):
                room.spaceoutcontent_set.add(contentModel)

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
        user.last_activity = datetime.now()
        user.save()
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

class AddPasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        user = request.user
        user.set_password(request.data["password"])
        user.is_verified = False
        user.save()
        send_signup_email(user, request)
        return Response(status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        if not "password" in request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        user.set_password(request.data["password"])
        user.save()
        return Response(status=status.HTTP_200_OK)

class CheckPasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        logged_in_user = request.user
        user = authenticate(email=logged_in_user.email, password=request.data['password'])
        if user == None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_200_OK)

class ChangeSpacerNameView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        user = request.user
        if "user_name" in request.data:
            try:
                spacer = SpaceoutUser.objects.get(user_name=request.data["user_name"])
                return Response({'code':6, 'debug':"Username already exist"}, status=status.HTTP_200_OK)
            except SpaceoutUser.DoesNotExist:
                user.user_name = request.data['user_name']
                user.save()
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SpaceoutUserSerializer

    def get(self, request, format=None):
        user = request.user
        user.last_activity = datetime.now()
        user.save()

        room = user.spaceoutroom_set.first()
        if room == None:
            roomDefinition = SpaceoutRoomDefinition.objects.get(
                type=SpaceoutRoomDefinition.ROOM_TYPE_HOME
            )
            room = SpaceoutRoom(user_id=user.id)
            room.definition = roomDefinition
            room.save()

        return Response(self.serializer_class(user).data)

    def post(self, request, format=None):
        user = request.user
        user.last_activity = datetime.now()

        for key in request.data:
            if key == 'facebook_id':
                if request.data['facebook_id'] != None and request.data['facebook_id'] != '':
                    user.facebook_id = request.data['facebook_id']
            if key == 'reddit_id':
                if request.data['reddit_id'] != None and request.data['reddit_id'] != '':
                    user.reddit_id = request.data['reddit_id']
            if key == 'soundcloud_id':
                if request.data['soundcloud_id'] != None and request.data['soundcloud_id'] != '':
                    user.soundcloud_id = request.data['soundcloud_id']
            if key == 'twitter_id':
                if request.data['twitter_id'] != None and request.data['twitter_id'] != '':
                    user.twitter_id = request.data['twitter_id']
            if key == 'notification_id':
                user.notification_id = request.data['notification_id']
            if key == 'latitude':
                user.latitude = request.data['latitude']
            if key == 'longitude':
                user.longitude = request.data['longitude']
            if key == 'first_name':
                user.first_name = request.data['first_name']
            if key == 'last_name':
                user.last_name = request.data['last_name']
            if key == 'fb_gender':
                user.fb_gender = request.data['fb_gender']
            if key == 'fb_location':
                user.fb_location = request.data['fb_location']
            if key == 'fb_birthdate':
                user.fb_birthdate = request.data['fb_birthdate']
            if key == 'avatar_url' and not user.featured:
                user.avatar_url = request.data['avatar_url']
            if key == 'personality_insights_input_url':
                if user.personality_insights_input_url != None:
                    user.personality_insights_input_url.storage.delete(user.personality_insights_input_url.name)
                user.personality_insights_input_url = request.FILES['personality_insights_input_url']
            if key == 'personality_insights_output_url':
                if user.personality_insights_output_url != None:
                    user.personality_insights_output_url.storage.delete(user.personality_insights_output_url.name)
                user.personality_insights_output_url = request.FILES['personality_insights_output_url']


        user.save()

        return Response(status=status.HTTP_200_OK)

class CommentView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        author = request.user
        author.last_activity = datetime.now()
        author.save()
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
        user = request.user
        user.last_activity = datetime.now()
        user.save()
        comment = SpaceoutComment.objects.get(id=request.data['comment_id'])
        if user.id == comment.author.id or user.id == comment.content.room.user.id:
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
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class NotificationsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        return Response(SpaceoutUserNotificationsSerializer(user).data)

    def post(self, request, format=None):
        user = request.user
        notification = SpaceoutNotification.objects.get(id=request.data['notification_id'])
        if(notification.user.id == user.id):
            notification.read = True
            notification.save()
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

class WatsonView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        watson_input = WatsonInput(
            user = request.user,
            chunk_id = request.data['chunk_id'],
            recipe_id = request.data['recipe_id'],
            chunk_date_start = request.data['start_date'],
            chunk_date_end = request.data['end_date'],
            data_size = request.data['data_size'],
            social_network = request.data['social_network'],
            watson_response_time = request.data['watson_response_time'],
            input_url=request.FILES['input'],
        )
        watson_input.save()

        results = json.loads(request.data['watson_result'])
        for result in results['result']:
            watson_output = WatsonOutput(
                text = result['text'],
                analysis = result['analysis'],
                relevance = result['relevance'],
                watson_input = watson_input
            )
            watson_output.save()

        return Response(status=status.HTTP_200_OK)

    def get(self, request, format=None):
        # clean watson data for user
        user = request.user
        user.last_activity = datetime.now()
        user.save()
        try:
            WatsonInput.objects.filter(user_id=user.id).delete()
        except:
            pass
        # return blacklist
        return Response(WatsonBlacklistSerializer(WatsonBlacklist.objects.all(), many=True).data)

class OnLineView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return self.query(request, request.query_params['page_size'], request.query_params['page'])
    def post(self, request, format=None):
        return self.query(request, request.data['page_size'], request.data['page'])

    def query(self, request, page_size, page):
        # users = SpaceoutUser.objects.order_by('-last_activity')
        users = users_with_room().order_by('-last_activity')

        paginator = Paginator(users, page_size) # Show 25 contacts per page

        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            result = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            result = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PeopleSeriaizer(result,
                                     context=serializer_context)
        return Response(serializer.data)

class PopularView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return self.query(request, request.query_params['page_size'], request.query_params['page'])
    def post(self, request, format=None):
        return self.query(request, request.data['page_size'], request.data['page'])

    def query(self, request, page_size, page):
        users = users_with_room().order_by('-popularity')
        # users = SpaceoutUser.objects.order_by('-popularity')

        paginator = Paginator(users, page_size) # Show 25 contacts per page

        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            result = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            result = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PeopleSeriaizer(result,
                                     context=serializer_context)
        return Response(serializer.data)



class FeaturedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return self.query(request, request.query_params['page_size'], request.query_params['page'])
    def post(self, request, format=None):
        return self.query(request, request.data['page_size'], request.data['page'])

    def query(self, request, page_size, page):
        users = users_with_room().filter(featured=True)
        # users = SpaceoutUser.objects.filter(featured=True)

        paginator = Paginator(users, page_size) # Show 25 contacts per page

        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            result = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            result = paginator.page(paginator.num_pages)

        serializer_context = {'request': request}
        serializer = PeopleSeriaizer(result,
                                     context=serializer_context)
        return Response(serializer.data)

class SearchView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        if 's' in request.query_params:
            if request.query_params['s'] == 's':
                # street view
                lat = request.query_params['lat']
                lon = request.query_params['lon']
                fov = request.query_params['fov']
                heading = request.query_params['h']
                pitch = request.query_params['p']
                url = settings.STREET_VIEW_API_URL % (lat, lon, fov, heading, pitch, settings.GOOGLE_API_KEY)
                r = requests.get(url, headers={'referer': 'spaceoutvr-prod.mybluemix.net'})
                return HttpResponse(r, content_type="image/jpeg")
            elif request.query_params['s'] == 'y':
                # youtube
                query = request.query_params['q']
                url = settings.YOUTUBE_SEARCH_URL % (query, settings.GOOGLE_API_KEY)
                if "pageToken" in request.query_params:
                    page_token = request.query_params['pageToken']
                    url = url + "&pageToken=%s" % page_token
                print(url)
                r = requests.get(url, headers={'referer': 'spaceoutvr-prod.mybluemix.net'})
                return Response(r.json())
        else:
            # google images
            query = request.query_params['q']
            url = "%s/?q=%s%s%s%s&safe=medium" % (settings.GOOGLE_SEARCH_BASE_URL, query, settings.GOOGLE_SEARCH_ENGINE_ID, settings.GOOGLE_SEARCH_URL, settings.GOOGLE_API_KEY)

            if "start" in request.query_params:
                start_page = request.query_params['start']
                url = url + "&start=%s" % start_page

            print(url)

            r = requests.get(url, headers={'referer': 'spaceoutvr-prod.mybluemix.net'})
            return Response(r.json())

class AuthenticateEmailResendView(GenericAPIView):
    def post(self, request, format=None):
        try:
            user = SpaceoutUser.objects.get(email=request.data["id"])
            send_signup_email(user, request)
            return Response({'code':4, 'debug':'Please check your email and click the link to verify your email addresss.\n Then tap the button below to continue.'}, status=status.HTTP_200_OK)
        except SpaceoutUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class AuthenticateEmailView(GenericAPIView):
    def post(self, request, format=None):
        print("SignIn - Email")
        password_provided = "password" in request.data
        spacer_name_provided = "user_name" in request.data

        print("password provided? %s" % password_provided)
        print("space name provided? %s" % spacer_name_provided)

        try:
            user = SpaceoutUser.objects.get(email=request.data["id"])
            # user exist, trying to login
            has_spacer_name = user.user_name != None and user.user_name != ''
            has_password = user.hasPassword()

            print("has spacer name? %s" % has_spacer_name)
            print("has password? %s" % has_password)

            if has_password:
                if password_provided:

                    if not user.is_verified:
                        return Response({'code':4, 'debug':'Please check your email and click the link to verify your email addresss.\n Then tap the button below to continue.'}, status=status.HTTP_200_OK)

                    # password was provided, login!
                    print("Login %s %s" % (request.data["id"], request.data["password"]))
                    if user.is_verified:
                        if has_spacer_name:
                            # delete old signup code
                            try:
                                signup_code = SignupCode.objects.get(user=user)
                                signup_code.delete()
                            except SignupCode.DoesNotExist:
                                pass

                            # Login
                            account = wrapper.Authemail()
                            account.base_uri = "%s/api" % settings.SERVER_URL
                            response = account.login(email=request.data["id"], password=request.data["password"])
                            if 'token' in response:
                                response['code'] = 0
                                response['debug'] = 'Logged in'
                                return Response(response, status=status.HTTP_200_OK)
                            else:
                                # not authorized
                                return Response(status=status.HTTP_401_UNAUTHORIZED)
                        else:
                            if spacer_name_provided:
                                # Login
                                account = wrapper.Authemail()
                                account.base_uri = "%s/api" % settings.SERVER_URL
                                response = account.login(email=request.data["id"], password=request.data["password"])
                                if 'token' in response:
                                    # save spacer name
                                    try:
                                        spacer = SpaceoutUser.objects.get(user_name=request.data["user_name"])
                                        return Response({'code':6, 'debug':"Username already exist"}, status=status.HTTP_200_OK)
                                    except SpaceoutUser.DoesNotExist:
                                        user.user_name = request.data["user_name"]
                                        user.save()
                                        response['code'] = 0
                                        response['debug'] = 'Logged in'
                                        return Response(response, status=status.HTTP_200_OK)
                                else:
                                    # not authorized
                                    return Response(status=status.HTTP_401_UNAUTHORIZED)
                            else:
                                # user has spacer name
                                return Response({'code':5, 'debug':"Create your Spacer Name (or use our suggestion) to finish creating your account"}, status=status.HTTP_200_OK)
                    else:
                        # user not verified
                        return Response({'code':4, 'debug':"Please check your email and click the link to verify your email addresss.\n Then tap the button below to continue."}, status=status.HTTP_200_OK)
                else:
                    # no password provided
                    return Response({'code':2, 'debug':"Email Sign In, enter your password"}, status=status.HTTP_200_OK)
            else:
                # user has no password, ask for a password
                return Response({'code':3, 'debug':"An account already exists for this email address.\n Please sign in using a method used before.\n (Once signied in, you can add a password in Account Settings menu.)"}, status=status.HTTP_200_OK)

        except SpaceoutUser.DoesNotExist:
            # user do not exist, trying to sign up
            if password_provided:
                new_user = SpaceoutUser.objects.create_user(email=request.data["id"])
                new_user.set_password(request.data["password"])
                new_user.save()

                send_signup_email(new_user, request)

                return Response({'code':4, 'debug':'Please check your email and click the link to verify your email addresss.\n Then tap the button below to continue.'}, status=status.HTTP_200_OK)

            return Response({'code':1, 'debug':'No account exists for this email address.\n Enter a new password to create a new account!'}, status=status.HTTP_200_OK)

class AuthenticateFacebookView(GenericAPIView):
    def post(self, request, format=None):
        print("SignIn - Facebook")

        access_token = request.data["id"]
        spacer_name_provided = "user_name" in request.data

        facebook = FacebookBackend()
        response = facebook.login(access_token)
        if 'token' in response:
            # logged in!
            return Response(response, status=status.HTTP_200_OK)

        # check if there is an old account with the facebook email
        data = facebook.get_token_data(access_token)
        try:
            fb_id = data['id']
            fb_email = data['email']
            try:
                existing_user = SpaceoutUser.objects.get(email=fb_email)
                existing_user.facebook_token = access_token
                existing_user.facebook_id = fb_id
                existing_user.save()

            except SpaceoutUser.DoesNotExist:
                if spacer_name_provided:
                    # signup
                    facebook.signup(
                        fb_email,
                        request.data["user_name"],
                        fb_id,
                        access_token
                    )
                else:
                    return Response({'code':5, 'debug':"Create your Spacer Name (or use our suggestion) to finish creating your account"}, status=status.HTTP_200_OK)

            # try to login
            token = facebook.login(access_token)
            if token != None:
                # logged in!
                return Response({'code':0, 'token': token, 'debug': 'Logged in'}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        except:
            print("access token not valid %s" % access_token)
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DebugView(GenericAPIView):
    serializer_class = SpaceoutUserSerializer

    def get(self, request, format=None):

        # with_fb = SpaceoutUser.objects.all().filter(facebook_id__isnull=False).count()
        # total = SpaceoutUser.objects.all().count()
        # report = "{'with_fb':%s, 'total':%s, 'rate':%s}" % (with_fb, total, total / with_fb)
        # return Response(report)

        user = SpaceoutUser.objects.all()
        return Response(SpaceoutUserSerializer(user, many=True).data)

        # room = SpaceoutRoom.objects.get(user_id=2)
        # return Response(SpaceoutRoomSerializer(room).data)

        # rooms = SpaceoutRoom.objects.all()
        # return Response(SpaceoutRoomSerializer(rooms, many=True).data)

        # storage = IBMObjectStorage()
        # storage.exists("lalala")
        # return Response(status=status.HTTP_200_OK)
    #
    # def post(self, request, format=None):
    #     author = SpaceoutUser.objects.get(id=2)
    #     content = SpaceoutContent.objects.get(id=20)
    #
    #     comment = SpaceoutComment(
    #         author=author,
    #         content=content,
    #         audio_file=request.FILES['file'],
    #     )
    #     comment.save()



        return Response(SpaceoutCommentSerializer(comment).data)
