# sso_server/authapp/views.py
import jwt
import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

JWT_SECRET = "secret_key"

USERS = {
    "admin_1": "password1",
    "admin_2": "password2"
}

@csrf_exempt 
def login_view(request):
    if request.method == "GET":
        redirect_uri = request.GET.get("redirect_uri", "")
        return render(request, "login.html", {"redirect_uri": redirect_uri})
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        redirect_uri = request.POST.get("redirect_uri", "")
        if username in USERS and USERS[username] == password:
            payload = {
                "sub": username,
                "iat": datetime.datetime.utcnow(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
            # Convert token to a string if it's returned as bytes
            if isinstance(token, bytes):
                token = token.decode("utf-8")
            # Redirect back to the client with the token
            return redirect(f"{redirect_uri}?token={token}")
        else:
            error = "Invalid credentials. Please try again."
            return render(request, "login.html", {"redirect_uri": redirect_uri, "error": error})
    else:
        return HttpResponseBadRequest("Unsupported HTTP method.")

def validate_token(request):
    token = request.GET.get("token")
    if not token:
        return JsonResponse({"valid": False, "error": "Token missing"}, status=400)
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return JsonResponse({"valid": True, "username": data["sub"]})
    except Exception as e:
        return JsonResponse({"valid": False, "error": str(e)}, status=401)