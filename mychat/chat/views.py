from ast import Return
from django.shortcuts import render
from django.http import JsonResponse
import random
import time
import json
from .models import RoomMember

from agora_token_builder import RtcTokenBuilder

from django.views.decorators.csrf import csrf_exempt

def chat(request):
    return render(request, 'chat.html')

def room(request):
    return render(request,'room.html')


def getToken(request):
    appId = 'f6830721f8294c67b8e64329157f1576'
    appCertificate = '6186d0575497424f8453bb80430bd365'
    channelName = request.GET.get('channel')
    uid = random.randint(1, 230)
    expirationTimeinSecond = 3600 * 24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeinSecond
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token,'uid':uid},safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member ,created = RoomMember.objects.get_or_create(
        name= data['name'],
        uid = data['UID'],
        room_name =data['room_name']
    )
    return JsonResponse({'name':data['name']},safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('uid')
    member = RoomMember.objects.get(
        uid= uid,
        room_name = room_name,
    )   
    name = member.name
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        name= data['name'],
        uid= data['UID'],
        room_name =data['room_name'],
    )
    member.delete()
    
    return JsonResponse('Member was deleted',safe=False)
