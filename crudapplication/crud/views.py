from django.conf import settings
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail

from crud.models import UserProfile
from crud.serializers import GetUserValidator, RegisterUserValidator, UserprofileSerializer
from crud.filters import make_user_filters


class SignupView(APIView):
    permission_classes = []
    authentication_classes = []
    parser_classes = [JSONParser]

    def post(self, request):
        try:
            response = {}
            api_request_body = request.data
            validation = RegisterUserValidator(data=api_request_body)
            if not validation.is_valid():
                response["success"] = False
                response["details"] = "Bad Request Body"
                response["errors"] = validation.errors
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

            username = api_request_body.get('username')
            phone = api_request_body.get('phone')
            email = api_request_body.get('email')
            password = api_request_body.get('password')
            city = api_request_body.get('city')
            country = api_request_body.get('country')
            zipcode = api_request_body.get('zipcode')
            address = api_request_body.get('address')
            device_type = api_request_body.get('device_type')
            first_name = api_request_body.get('first_name')
            last_name = api_request_body.get('last_name')

            if User.objects.filter(Q (username__iexact=username) | Q (email__iexact=email)).exists():
                response["success"] = False
                response["details"] = "Validation failed"
                response["errors"] = "Data duplicate"
                return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)

            if UserProfile.objects.filter(phone=phone).exists():
                response["success"] = False
                response["details"] = "Validation failed"
                response["errors"] = "Data duplicate"
                return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    last_name=last_name,
                    first_name=first_name
                )
                api_request_body['user_id'] = user.id
                response["success"] = True
                response["details"] = "User registred successfully"
                response["errors"] = ""
                UserProfile.objects.create(
                    phone=phone,
                    city=city,
                    country=country,
                    zipcode=zipcode,
                    user_id=user.id,
                    device_type=device_type,
                    address=address
                )
                subject = 'New User Registration'
                message = 'Thank you for registering with our portal. We are glad to have in our community'
                send_mail(
                    subject, message, settings.EMAIL_HOST_USER, [user.email],
                    fail_silently=False)
                return Response(data=response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response["success"] = True
            response["details"] = "Exception occurred"
            response["errors"] = str(e)
            return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)

class LoginView(APIView):
    permission_classes = []
    authentication_classes = []
    parser_classes = [JSONParser]

    def post(self, request):
        response = {}
        api_request_body = request.data
        username = api_request_body.get("username")
        password = api_request_body.get("password")
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                response["success"] = True
                response["details"] = "Login success"
                response["errors"] = ""
                response["token"] = token.key
                return Response(data=response, status=status.HTTP_200_OK)
            response["success"] = False
            response["details"] = "Invalid Credentials"
            response["errors"] = ""
            return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)
        except Exception as e:
            response["success"] = False
            response["details"] = "Exception while user login"
            response["errors"] = str(e)
            return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)


class CRUDView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get(self, request):
        response = {}
        try:
            user = UserProfile.objects.get(user_id=request.user.id)
            response["success"] = True
            response["details"] = ""
            response["errors"] = ""
            response["data"] = UserprofileSerializer(user, many=False).data
            return Response(data=response, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist as e:
            response["success"] = False
            response["details"] = "User does not exist"
            response["errors"] = str(e)
            return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)
        except Exception as e:
            response["success"] = True
            response["details"] = "Exception occured in CRUDView"
            response["errors"] = str(e)
            return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)


    def put(self, request):
        response = {}
        try:
            api_request_body = request.data
            user_profile = UserProfile.objects.get(user_id=request.user.id)
            phone = api_request_body.get("phone")
            first_name = api_request_body.get("first_name")
            last_name = api_request_body.get("last_name")
            email = api_request_body.get("email")
            city = api_request_body.get("city")
            country = api_request_body.get("country")
            district = api_request_body.get("district")
            address = api_request_body.get("address")
            zipcode = api_request_body.get("zipcode")

            if phone:
                if UserProfile.objects.exclude(id=user_profile.id).filter(phone=phone).exists():
                    response = {}
                    response["success"] = False
                    response["details"] = "Phone exists"
                    response["errors"] = "Phone exists"
                    return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)
                user_profile.phone = phone
            if first_name:
                user_profile.user.first_name = first_name
            if last_name:
                user_profile.user.last_name = last_name
            if email:
                if User.objects.filter(email__iexact=email).exists():
                    response = {}
                    response["success"] = False
                    response["details"] = "Email exists"
                    response["errors"] = "Email exists"
                    return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)
                user_profile.user.email = email
            if city:
                user_profile.city = city
            if country:
                user_profile.country = country
            if district:
                user_profile.district = district
            if address:
                user_profile.address = address
            if zipcode:
                user_profile.zipcode = zipcode

            user_profile.user.save()
            user_profile.save()

            response["success"] = True
            response["details"] = "Data updated"
            response["errors"] = ""
            return Response(data=response, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist as e:
            response["success"] = False
            response["details"] = "User does not exist"
            response["errors"] = str(e)
            return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)
        except Exception as e:
            response["success"] = True
            response["details"] = "Exception occured in CRUDView"
            response["errors"] = str(e)
            return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)

    def delete(self, request):
        response = {}
        try:
            User.objects.filter(id=request.user.id).delete()
            response["success"] = True
            response["details"] = "User deleted"
            response["errors"] = ""
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            response["success"] = False
            response["details"] = "User not found"
            response["errors"] = str(e)
            return Response(data=response, status=status.HTTP_412_PRECONDITION_FAILED)


class GetUsersView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def get(self, request):
        response = {}
        kwargs = make_user_filters(request.data)
        queryset = UserProfile.objects.filter(**kwargs)
        response["success"] = True
        response["details"] = ""
        response["errors"] = ""
        response["data"] = UserprofileSerializer(queryset, many=True).data
        return Response(data=response, status=status.HTTP_200_OK)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]

    def delete(self, request):
        response = {}
        Token.objects.filter(user=request.user).delete()
        response["success"] = True
        response["details"] = "Token removed successfully"
        response["errors"] = ""
        return Response(data=response, status=status.HTTP_200_OK)