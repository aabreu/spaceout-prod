from django.conf.urls import url
from django.conf import settings
from spaceoutvr import views

urlpatterns = [
    url(r'^api/accounts/authenticate/facebook/$', views.AuthenticateFacebookView.as_view(), name='fb_authenticate'),

    url(r'^api/accounts/profile/$', views.ProfileView.as_view(), name='me'),
    url(r'^api/accounts/friends/$', views.FriendsView.as_view(), name='get_contacts'),
    url(r'^api/accounts/people/online/$', views.OnLineView.as_view(), name='people_online'),
    url(r'^api/accounts/people/popular/$', views.PopularView.as_view(), name='people_popular'),
    url(r'^api/accounts/people/featured/$', views.FeaturedView.as_view(), name='people_featured'),
    url(r'^api/accounts/room/$', views.RoomView.as_view(), name='room'),
    url(r'^api/accounts/comment/$', views.CommentView.as_view(), name='comment'),
    url(r'^api/accounts/content/$', views.ContentView.as_view(), name='content'),
    url(r'^api/accounts/notifications/$', views.NotificationsView.as_view(), name='notifications'),
    url(r'^api/accounts/watson/$', views.WatsonView.as_view(), name='watson'),
    url(r'^api/accounts/search/$', views.SearchView.as_view(), name='search'),
    url(r'^api/accounts/debug/$', views.DebugView.as_view(), name='debug'),

    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': True,
        }),
    # url(r'^landing/$', views.LandingView.as_view(), name='landing_page'),
    #
    # url(r'^signup/$', views.SignupView.as_view(), name='signup_page'),
    # url(r'^signup/email_sent/$', views.SignupEmailSentView.as_view(),
    #     name='signup_email_sent_page'),
    url(r'^signup/verify/$', views.SignupVerifyView.as_view()),
    url(r'^signup/verified/$', views.SignupVerifiedView.as_view(),
        name='signup_verified_page'),
    url(r'^signup/not_verified/$', views.SignupNotVerifiedView.as_view(),
        name='signup_not_verified_page'),
    #
    # url(r'^login/$', views.LoginView.as_view(), name='login_page'),
    # url(r'^home/$', views.HomeView.as_view(), name='home_page'),
    # url(r'^logout/$', views.LogoutView.as_view(), name='logout_page'),
    #
    url(r'^password/reset/$', views.PasswordResetVerifyView.as_view(),
        name='password_reset_page'),
    url(r'^password/reset/email_sent/$',
        views.PasswordResetEmailSentView.as_view(),
        name='password_reset_email_sent_page'),
    url(r'^password/reset/verify/$', views.PasswordResetVerifyView.as_view()),
    url(r'^password/reset/verified/$',
        views.PasswordResetVerifiedView.as_view(),
        name='password_reset_verified_page'),
    url(r'^password/reset/not_verified/$',
        views.PasswordResetNotVerifiedView.as_view(),
        name='password_reset_not_verified_page'),
    url(r'^password/reset/success/$', views.PasswordResetSuccessView.as_view(),
        name='password_reset_success'),

    url(r'^password/change/$', views.PasswordChangeView.as_view(),
        name='password_change_page'),

        ]
