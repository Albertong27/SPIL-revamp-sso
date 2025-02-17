from django.shortcuts import redirect, render, HttpResponse
import requests

SSO_SERVER = "http://localhost:8000"

def home(request):
    username = request.session.get("username")
    if username:
        return render(request, "home.html", {"username": username})
    else:
        return render(request, "login_client.html")

def login(request):
    callback_url = request.build_absolute_uri("/callback/")
    return redirect(f"{SSO_SERVER}/login/?redirect_uri={callback_url}")

def callback(request):
    token = request.GET.get("token")
    print("Received token:", token)  # This prints the token to your console for debugging

    if not token:
        return HttpResponse("No token provided", status=400)
    
    validate_url = f"{SSO_SERVER}/validate/?token={token}"
    response = requests.get(validate_url)
    print("Validation response:", response.status_code, response.text)  # Debug output

    if response.status_code == 200:
        data = response.json()
        if data.get("valid"):
            request.session["username"] = data["username"]
            return redirect("/")
        else:
            return HttpResponse("Token is not valid", status=401)
    else:
        return HttpResponse("Validation request failed", status=response.status_code)

def logout(request):
    request.session.flush()
    return redirect("/")

