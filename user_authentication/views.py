import re
from django.http.response import HttpResponseBadRequest
from matplotlib.style import use
from rest_framework.response import Response
from django.contrib.auth.models import User


from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["POST"])
def register(request):
    data = request.data
    first_name  = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]
    password = data["password"]
    user = User.objects.create(username = first_name+" "+last_name , email = email)
    if user:
        user.set_password(password)
        user.save()
        return Response("User created")
    else:
        return  HttpResponseBadRequest("Some error occured")



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(["POST"])
def login(request):
    try:
        data = request.data
        email = data["email"]
        password = data["password"]
        user = User.objects.get(email=email)
        if user.check_password(password):
            tokens = get_tokens_for_user(user)
            response = Response({'access_token':tokens['access']})
            print(response)
            response.set_cookie('referesh_token',tokens['refresh'],httponly=True)
            return response
        else:
            return HttpResponseBadRequest("Incorrect password")
    except User.DoesNotExist:
        return HttpResponseBadRequest("Invalid email")
    except:
        return HttpResponseBadRequest("Authentication failed")

@api_view(['GET'])
def hello(request):
    cookie = request.COOKIES.get('referesh_token')
    mgs = "the cookie that backend got is "+str(cookie)
    return Response(mgs) 

