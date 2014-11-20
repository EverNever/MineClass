from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mineclass.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    #API: users
    url(r'^api/createuser$','main.views.Render_API_CreateUser'),
    url(r'^api/updateselfinfo$','main.views.Render_API_UpdateSelfInfo'),
    url(r'^api/login$','main.views.Render_API_Login'),
    url(r'^api/logout$','main.views.Render_API_Logout'),
    url(r'^api/getuserinfo$','main.views.Render_API_GetUserInfo'),
    url(r'^api/getuserinfobyusername$','main.views.Render_API_GetUserInfoByUsername'),
    url(r'^api/setuserpriority$','main.views.Render_API_SetUserPriority'),
    url(r'^api/deleteuser$','main.views.Render_API_DeleteUser'),

    #API: class info
    url(r'^api/createclass$','main.views.Render_API_CreateClass'),
    url(r'^api/getclassinfobyindex$','main.views.Render_API_GetClassInfoByIndex'),
    url(r'^api/getallclassinfo$','main.views.Render_API_GetAllClassInfo'),
    url(r'^api/deleteclassbyindex$','main.views.Render_API_DeleteClassByIndex'),

    #API: announcements

    url(r'^api/publishannouncement$','main.views.Render_API_PublishAnnouncement'),
    url(r'^api/getannouncements$','main.views.Render_API_GetAnnouncements'),
    url(r'^api/deleteannouncement$','main.views.Render_API_DeleteAnnouncement'),
    url(r'^api/markasread$','main.views.Render_API_API_MarkAsRead'),

    #API: UploadFile

    url(r'^api/upload$','main.views.Render_API_UploadFile'),

    #API: Treehole

    url(r'^api/publishtreehole$','main.views.Render_API_PublishTreehole'),
    url(r'^api/gettreehole$','main.views.Render_API_GetTreehole'),

    #API: Comments

    url(r'^api/publishcomment$','main.views.Render_API_PublishComment'),
    url(r'^api/getcommentsbyid$','main.views.Render_API_GetCommentsByID'),
    url(r'^api/deletecommentbyid$','main.views.Render_API_DeleteCommentByID'),


    #Testing page
    url(r'^apitest$','main.views.Render_APITest'),
    url(r'^home_page$','main.views.Render_Index'),
    url(r'^setinfo$','main.views.Render_SetInfo'),
    url(r'^sethead$','main.views.Render_SetHead'),
    url(r'^setpassword$','main.views.Render_SetPassword'),
    url(r'^inform$','main.views.Render_Inform'),
    url(r'^discuss$','main.views.Render_Discuss'),
    url(r'^login$','main.views.Render_Login'),
    url(r'^regist$','main.views.Render_Regist'),
)
