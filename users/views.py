from django.contrib.auth import login, logout
from django.http import JsonResponse

from .models import User


def login_view(request):

    if request.user.is_anonymous:
        try:
            user = User.objects.get(username=request.POST.get("username"))
            if user.check_password(request.POST.get("password")):
                login(request, user)
                return JsonResponse(
                    {
                        "detail": "success",
                        "request_session": request.session.session_key,
                        "username": request.user.username,
                    }
                )
        except User.DoesNotExist:
            return JsonResponse({"detail": "failed"})

    return JsonResponse({"detail": "failed", "message": "Ви вже увійшли в систему."})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({"detail": "success"})
    return JsonResponse({"detail": "failed", "message": "Ви не ввійшли в систему."})
