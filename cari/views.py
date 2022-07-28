from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .models import User, Result

# serializers
from .serializers import UserSerializer, ResultSerializer

# email
from django.core.mail import BadHeaderError, send_mail
from .email import send_email
from pathlib import Path
import shutil, os

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

# run AImodel
from . import StyleCariGAN
from . import StyleCLIP

def get_result(user_id):
    try:
        result = Result.objects.filter(user_id=user_id)
        return result
    except Result.DoesNotExist:
        raise Http404


# user_id에 맞는 사용자 정보 가져옴
def get_user(user_id):
    try:
        user = User.objects.get(user_id=user_id)
        return user
    except User.DoesNotExist:
        raise Http404        


class UserInfo(APIView):
    def post(self, request):
        user_img = request.FILES.get("image")
        if user_img:
            user = User(user_img=user_img)
            user.save()
            serializer = UserSerializer(user)

            # save user image in another directory
            src = '/home/teamg/volume/CarryCARI-BE/_media/{filename}'.format(filename=user.user_img.name)
            # src = './_media/{filename}'.format(filename=user.user_img.name)

            # make directory
            dest = "/home/teamg/volume/CarryCARI-BE/assets/user_img/{user_id}".format(user_id=user.user_id)
            # dest = "./assets/user_img/{user_id}".format(user_id=user.user_id)
            os.makedirs(dest)

            # copy to new directory
            shutil.copy(src, dest)

            return Response(serializer.data, status=200)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class SendEmail(APIView):

    def post(self, request):
        user_id = request.data.get("user_id")
        user_email = request.data.get("user_email")

        print(user_id)
        print(user_email)

        user = get_user(user_id)
        user.user_email = user_email
        user.save()

        return Response({
            "save": user.user_email
        })


class ResultDetail(APIView):

    def get(self, request):
        user_id = request.query_params.get('id')
        emotion = int(request.query_params.get('emotion'))
        user = User.objects.get(user_id=user_id)

        before_img = get_user(user_id).user_img.url

        if emotion == 0: #stylecarigan만 실행
            print("======func1======")
            print("StyleCariGAN만 실행...")
            StyleCariGAN.run_StyleCariGAN(user, user_id, emotion)
        else: #styleclip -> stylecarigan 실행
            print("======func2, emotion = " + str(emotion) +"======")
            print("StyleCLIP 실행...")
            StyleCLIP.run_StyleCLIP(user, user_id, emotion)
            print("StyleCariGAN 실행...")
            StyleCariGAN.run_StyleCariGAN(user, user_id, emotion)

        result_image_path = '/home/teamg/volume/CarryCARI-BE/ml/StyleCariGAN/final_result/' 
        os.makedirs('/home/teamg/volume/CarryCARI-BE/_media/result_images/{user_id}'.format(user_id=user_id))
        file_list = os.listdir(result_image_path)

        for item in file_list:
            result = Result()
            result.user_id = User.objects.get(user_id=user_id)
            image_path = f'/home/teamg/volume/CarryCARI-BE/ml/StyleCariGAN/final_result/{item}' 
            upload_path = f'/home/teamg/volume/CarryCARI-BE/_media/result_images/{user_id}/{item}'

            shutil.copy(image_path, upload_path)
            result.result_img_path = '/_media/result_images/{user_id}/{item}'.format(user_id=user_id, item=item)

            result.result_emotion = emotion
            result.save()

        # user_email이 ""이 아닌경우(email을 등록한 경우) 결과를 메일로 전송
        user = get_user(user_id)
        if user.user_email != "":
            result = get_result(user_id) 

            image_path_list = []
            for item in result:
                image_path_list.append(item.result_img_path)

            print(image_path_list) 

            send_email(recipient=user.user_email, image_path_list=image_path_list)
            print("메일 전송 완료")

        result = get_result(user_id) 

        return Response({
            "before_img": before_img,
            "after_img_1": result[0].result_img_path,
            "after_img_2": result[1].result_img_path,
            "after_img_3": result[2].result_img_path,
            "after_img_4": result[3].result_img_path,
            "after_img_5": result[4].result_img_path,
            "after_img_6": result[5].result_img_path,
            "after_img_7": result[6].result_img_path,
            "after_img_8": result[7].result_img_path
        })