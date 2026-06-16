from django.contrib.auth import views as auth_view
from accounts.forms import AuthenticationForm
from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tasks import send_password_reset_email_task
from django.contrib.auth import get_user_model
from django.contrib import messages

User=get_user_model()

class LoginView (auth_view.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
class LogoutView(auth_view.LogoutView):
    pass

def reset_password(request):
    if request.method == "POST":

        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        print(user)

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = f"http://127.0.0.1:8000/accounts/reset-password-set/{uid}/{token}/"

            subject = "Reset Password Link"

            send_password_reset_email_task.delay(
                subject,
                reset_link,
                [user.email],
            )

        messages.success(
            request,
            "If the email exists, a reset link has been sent."
        )

        return redirect("accounts:login")

    return render(request, "accounts/reset_password.html")
def new_password_set(request, uid, token):
    try:
        user_id = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=user_id)
    except:
        messages.error(request, "Invalid link")
        return redirect("accounts:login")

    

    if not default_token_generator.check_token(user, token):
        messages.error(request, "Invalid or expired link")
        return redirect("accounts:login")

    if request.method == "POST":

        new_password = request.POST.get("newPassword")
        confirm_new_password = request.POST.get("confirmNewPassword")

        if new_password != confirm_new_password:
            messages.error(request, "Passwords do not match")
            return render(request, 'accounts/new_password_set.html')

        if len(new_password) < 8:
            messages.error(request, "Password too short")
            return render(request, 'accounts/new_password_set.html')

        user.set_password(new_password)
        user.save()

        messages.success(request, "Password changed successfully")
        return redirect("accounts:login")

    return render(request, 'accounts/new_password_set.html')