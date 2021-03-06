from main.models import *
from main.escape import *
import time
from django.shortcuts import render_to_response
from django.http import HttpResponse
from mongoengine import *
import random
from main.api_users import *
import json

#API_PublishAnnouncement(request) Publish announcement
#Input parameters: HttpRequest Object : POST data
#Return value: HttpResponse Object
def API_PublishAnnouncement(request):
	if (not VerifyToken(request)):
		return HttpResponse('{"code":0,"message":"AccessToken invalid. Please login first."}',{})
	if (request.POST.get("announcement")==None or request.POST.get("announcement")==''):
		return HttpResponse('{"code":1,"message":"Empty content."}',{})
	dbobj = announcements()
	dbobj.PublishmentTime = int(time.time())
	dbobj.announcement = QuoteContent(request.POST.get("announcement"))
	dbobj.publisher = GetUsernameByToken(request.COOKIES.get("accesstoken"))
	if (request.POST.get("attachment")==None or request.POST.get("attachment")=='none' or request.POST.get("attachment")==''):
		dbobj.attachment = 'none'
	else:
		dbobj.attachment = QuoteEscapeContent(request.POST.get('attachment'))
	tags = []
	if (len(request.POST.getlist('tag[]'))>0):
		for SingleTag in request.POST.getlist('tag[]'):
			tags.append(QuoteEscapeContent(SingleTag))
	dbobj.tag = tags

	classes = []
	username = GetUsernameByToken(request.COOKIES.get("accesstoken"))
	userobj = users.objects(username=username).first()
	if (userobj.priority<=1):
		classes.append(userobj.classindex)
	else:
		if (len(request.POST.getlist('class[]'))>0):
			for classindex in request.POST.getlist('class[]'):
				classes.append(classindex)
		else:
			classes.append(userobj.classindex)
	ReadUsers = []
	ReadUsers.append(GetUsernameByToken(request.COOKIES.get("accesstoken")))
	dbobj.ReadUsers = ReadUsers
	dbobj.classes = classes
	dbobj.save()
	return HttpResponse('{"code":2,"message":"Success."}')

#API_GetAnnouncements(request) Get list of announcements
#Input parameters: HttpRequest Object : GET data
#Return value: HttpResponse Object
def API_GetAnnouncements(request):
	if (not VerifyToken(request)):
		return HttpResponse('{"code":0,"message":"AccessToken invalid. Please login first."}',{})
	username = GetUsernameByToken(request.COOKIES.get("accesstoken"))
	userclass = users.objects(username=username).first().classindex
	page = request.GET.get("page")
	if (page==None or page==""):
		dbobj = announcements.objects(classes=userclass).order_by("-PublishmentTime").all()
	else:
		dbobj = announcements.objects(classes=userclass).order_by("-PublishmentTime").skip((int(page)-1)*20).limit(20)
	AnnouncementList = []
	for RowObj in dbobj:
		if (len(request.GET.getlist('tag[]'))>0):
			for SingleTag in RowObj.tag:
				if (SingleTag in request.GET.getlist('tag[]')):
					AnnouncementList.append(eval(RowObj.to_json()))
					break
		else:
			AnnouncementList.append(eval(RowObj.to_json()))

	FixedList = []
	for SingleObj in AnnouncementList:
		publisher = SingleObj["publisher"]
		dbobj = users.objects(username=publisher)
		if (dbobj.count()>0):
			NewObj = SingleObj
			NewObj["publisher_realname"] = dbobj.first().realname
			NewObj["publisher_avatar"] = dbobj.first().avatar
		else:
			NewObj = SingleObj
			NewObj["publisher_realname"] = "USER_DELETED"
			NewObj["publisher_avatar"] = "static/upload/avatars/none.png"
		FixedList.append(NewObj)

	return HttpResponse(json.dumps(FixedList),{})

#API_DeleteAnnouncement(request) Delete announcement specified by id
#Input parameters: HttpRequest Object : GET data
#Return value: HttpResponse Object
def API_DeleteAnnouncement(request):
	if (not VerifyToken(request)):
		return HttpResponse('{"code":0,"message":"Please login first."}')
	if (request.GET.get("id")==None or request.GET.get("id")==""):
		return HttpResponse('{"code":1,"message":"Invalid input"}')
	username = GetUsernameByToken(request.COOKIES.get("accesstoken"))
	userobj = users.objects(username=username).first()
	userclass = userobj.classindex
	userpriority = userobj.priority
	annobj = announcements.objects(id=request.GET.get("id"))
	if (annobj.count()==0):
		return HttpResponse('{"code":2,"message":"Invalid id"}')

	if (userpriority==0 and username!=annobj.first().publisher):
		return HttpResponse('{"code":3,"message":"Permission denied."}')
	if (userpriority<=1):
		classlist = annobj.first().classes
		index = 0
		for SingleClass in classlist:
			if (SingleClass==userclass):
				del classlist[index]
				break
			index = index + 1
		annobj.update(set__classes=classlist)
	elif (userpriority>=2):
		annobj.delete()
	return HttpResponse('{"code":4,"message":"Success in deleting announcement."}')

#API_MarkAsRead(request) Mark an announcement as read by user
#Input Parameters: HttpRequest Object : Get data
#Return Value: HttpResponse Object
def API_MarkAsRead(request):
	if (not VerifyToken(request)):
		return HttpResponse('{"code":0,"message":"Please login first."}')
	if (request.GET.get("id")==None or request.GET.get("id")==""):
		return HttpResponse('{"code":1,"message":"Invalid input"}')
	annobj = announcements.objects(id=request.GET.get("id"))
	if (annobj.count()==0):
		return HttpResponse('{"code":2,"message":"Invalid id"}')
	ReadUsersList = []
	row = annobj.first()
	for ReadUser in row.ReadUsers:
		ReadUsersList.append(ReadUser)
	username = GetUsernameByToken(request.COOKIES.get("accesstoken"))
	if (not username in ReadUsersList):
		ReadUsersList.append(username)
	annobj.update(set__ReadUsers=ReadUsersList)
	return HttpResponse('{"code":3,"message":"Success."}')
