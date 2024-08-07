from rest_framework.response import Response
from django.contrib.auth import  login
from rest_framework.views import APIView
from .models import CustomUser
from rest_framework import status
from UserProfileapp.models import BasicDetails,FamilyDetails,LocationDetails,ProfessionalsDetails,ReligionInformation,Gallary,PatnerPreferences
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from .models import generate_otp
from .utils import convertjwt
from .serializers import CustomUserSerializer
from datetime import datetime
from UserProfileapp.serializer import Gallaryseializer,BasicDetailseializer
import base64
from django.core.files.base import ContentFile
from chatapp.models import Notifications

# Create your views here.

# customization for the token 
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        return token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer





# registration of the user 
class UserRegistration(APIView):
            def post(self, request):
                        if CustomUser.objects.filter(email = request.data['email']).exists():
                                    return Response({"error": "emailused"},status=status.HTTP_400_BAD_REQUEST)
                        if len(request.data['phone']) != 10:
                                    return Response({"error": "phonenumber"},status=status.HTTP_400_BAD_REQUEST)
                        gender = gender= request.data['gender']
                        if gender == "male":
                              gender_in_maintable = True
                        else:
                              gender_in_maintable = False
                        user = CustomUser(username = request.data['name'],email = request.data['email'],password = make_password(request.data['password']),phone = request.data['phone'],about_groom = request.data['about'],is_blocked = False,is_verified = False,account_for =  request.data['accountFor'],male = gender_in_maintable)
                        user.save()
                        current_user = CustomUser.objects.get(id = user.id)
                        current_date = datetime.now()
                        dobofuser_str = request.data['dob']
                        dobofuser = datetime.fromisoformat(dobofuser_str)  
                        age = current_date.year - dobofuser.year - ((current_date.month, current_date.day) < (dobofuser.month, dobofuser.day))
                        BasicDetails.objects.create(user_id = current_user,marital_status =request.data['maritalStatus'],dob=request.data['dob'],height=request.data['height'],mother_toungue= request.data['language'],gender= request.data['gender'],age = age)
                        ReligionInformation.objects.create(user_id = current_user,religion=request.data['religion'],cast=request.data['cast'])
                        FamilyDetails.objects.create(user_id = current_user,family_status=request.data['familystatus'])
                        ProfessionalsDetails.objects.create(user_id = current_user,employed_in=request.data['employed_in'],annual_income=request.data['annual_income'])
                        LocationDetails.objects.create(user_id = current_user,contry=request.data['country'],state=request.data['state'],district=request.data['district'])
                        Gallary.objects.create(user_id = current_user)
                        PatnerPreferences.objects.create(user_id = current_user)

                        return Response({"message": "Signup successful"},status=status.HTTP_201_CREATED)
            # taking data to front end
            def get(self ,request):
                  token = request.headers.get('Authorization')
                  lookupUserid = request.META.get('HTTP_LOOKUPUSERID', None)
                  user_id ,email = convertjwt(token)
                  if lookupUserid is not None:
                        user1 = CustomUser.objects.get(id = lookupUserid)
                        current_user = CustomUser.objects.get(id = user_id)
                        subscribed = current_user.subscribed
                        if not user1.is_superuser:
                              user_gallary = Gallary.objects.get(user_id = user1)
                              user_basic_details = BasicDetails.objects.get(user_id = user1)
                              usedetailsserializer = CustomUserSerializer(user1)
                              photoserializer = Gallaryseializer(user_gallary)
                              basicuserserializer = BasicDetailseializer(user_basic_details)
                              return Response({"message": "success","user":usedetailsserializer.data,"usergallary":photoserializer.data,"basicdetails":basicuserserializer.data,"subscribed":subscribed})
                  elif lookupUserid is  None:
                        user = CustomUser.objects.get(id = user_id)
                        usedetailsserializer = CustomUserSerializer(user)
                        if not user.is_superuser:
                              notification_count = Notifications.objects.filter(receiver = user,seen = False).count()
                              user_gallary = Gallary.objects.get(user_id = user)
                              user_basic_details = BasicDetails.objects.get(user_id = user)
                              usedetailsserializer = CustomUserSerializer(user)
                              photoserializer = Gallaryseializer(user_gallary)
                              basicuserserializer = BasicDetailseializer(user_basic_details)
                              return Response({"message": "Success","user":usedetailsserializer.data,"usergallary":photoserializer.data,"basicdetails":basicuserserializer.data,"notification_count":notification_count})
                        return Response({"message": "success","user":usedetailsserializer.data})


      #      function for the edit the data in the main details in  user profile
            def put(self,request):
                  token = request.headers.get('Authorization')
                  user_id ,email = convertjwt(token)
                  user = CustomUser.objects.get(id = user_id)
                  if "name" in request.data.keys():
                      name1 = request.data['name']
                      user.username = name1
                      user.save()
                  if request.data.get('image1'):
                        userdetails = Gallary.objects.get(user_id = user)
                        image1_file = request.data.get('image1')
                        format, imgstr = image1_file.split(';base64,')
                        ext = format.split('/')[-1]
                        image_file = ContentFile(base64.b64decode(imgstr), name=f'image1.{ext}')
                        setattr(userdetails, "image1", image_file)
                        userdetails.save()
                  if request.data.get('about'):
                        user.about_groom = request.data.get('about')
                        user.save()
                  return Response({"message": "success"},status=status.HTTP_201_CREATED)
                   

    
    




# after the registration otp verification
class Otpverificaion(APIView):
        def post(self,request):
            try:
              user = CustomUser.objects.get(email = request.data["email"])
            except:
                return Response({"error": "notpresent"},status=status.HTTP_400_BAD_REQUEST)
            if user.otp == int(request.data['otpValue']):
                  user.is_verified = True
                  user.save()
                  return Response({"message": "verified succesfully"},status=status.HTTP_201_CREATED)
            return Response({"error": "faild"},status=status.HTTP_400_BAD_REQUEST)



# login of the user
class Login(APIView):
      def post(self , request):
            email = request.data['email']
            password = request.data['password']
            try:
                  user = CustomUser.objects.get(email = email)
            except:
                  return Response({"error":"notpresent"},status=status.HTTP_400_BAD_REQUEST)
            if user and user.check_password(password) :
                  if user.is_superuser:
                         return Response({"message":"adminfound","role":"admin"},status=status.HTTP_200_OK)
                  else:
                       if user.is_verified:
                             if not user.is_blocked:
                                  login(request, user)
                                  return Response({"message":"userfound","role":"user",'id':user.id},status=status.HTTP_200_OK) 
                             else:
                              return Response({"error":"blocked"},status=status.HTTP_400_BAD_REQUEST) 
                                   
                       else: 
                             subject  = "Your otp for verification "
                             otp = generate_otp()
                             message = f'Your OTP is: {otp}. Please do not share this OTP.'
                             from_email = 'muhammedmamu2906@gmail.com' 
                             recipient_list = [email]
                             send_mail( subject,message,from_email,recipient_list, fail_silently=False)
                             user.otp = otp
                             user.save()
                             return Response({"error":"notverified"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"error":"notpresent"},status=status.HTTP_400_BAD_REQUEST)





