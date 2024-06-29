from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from .serializers import SysAdmin
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie,csrf_protect
from rest_framework.views import APIView
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from .tokens import *
# Create your views here.

# @api_view(['GET','POST'])
# def rejester(request):
#     if request.method == 'GET':
#         user=User.objects.all()
#         serializer=SysAdmin(user,many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         data=request.data
#         seralizer=SysAdmin(data=data)
#         print(seralizer)
#         if seralizer.is_valid():
#             seralizer.save()
#             use=seralizer.data
#             print(use)
#             # User.objects.create_user(username=use["username"],password=use["password"])
#             return Response(status=status.HTTP_201_CREATED)
#         else:
#             print(data)
#             return Response(status=status.HTTP_400_BAD_REQUEST)
def activate(request,uidb64,token):
    User = get_user_model()
    uid = force_str(urlsafe_base64_decode(uidb64))

    # print(uid)
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        newuser={"id":user.id,"is_active":user.is_active,"username":user}
        print(newuser)
    except:
        user = None
        print(user)
    print(newuser)
    print(user)
    
    if newuser["username"] is not None and account_activation_token.check_token(newuser,token):
        print(user)
        print(user.pk)
        user.is_active = True
        print(user.is_active)
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        print("True")
        # return HttpResponse("success")
    else:
        messages.error(request, "Activation link is invalid!")

    return HttpResponse("success")


def activateEmail(request,user,to_email):
    print(user)
    print(to_email)
    print(user)
    # print(to_email)
    mail_subject = 'Activate your user account.'
    message=render_to_string("template_activate.html",{

        'user':user['username']    ,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user['id'])),
        'token':account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',


    })
    email=EmailMessage(mail_subject,message,to=[to_email])
    if email.send():
        messages.success(request,f'Dear<b>{user}</b> please go to your <b>{to_email}</b> and click on received activation link to confirm and complete the registration')

    else:
        messages.error(request,f'Problem sending confirmation email to <b>{to_email}</b>, check')











class rejester(APIView):
    def post(self, request):
        serializer = SysAdmin(data=request.data)
        data=request.data
        print(data)
        if serializer.is_valid():
            serializer.save()
            use=serializer.data
            use["is_active"]=False
            print(use["is_active"])
            activateEmail(request,use,use['email'])
            return Response(use, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET','POST'])
def signin(request):
    em=[]
    user=User.objects.all()
    for i in user:
      em.append({'username':i.username,
                 'password':i.password
                 })
    if request.method == 'GET':
        return Response(em)
    if request.method == 'POST':
        data = request.data
        print(data)
        myuser=User.objects.filter(username=data['username'])
        user={"username":myuser[0].username,"password":myuser[0].password}
        print(user)
        auth=authenticate(username=user["username"],password=data["password"])
        print(auth)
        if auth is not None:
            login(request,auth)
            return Response(user,status=status.HTTP_200_OK)
        else:
            return Response({"user not found "})
        