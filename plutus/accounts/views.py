from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import LoginForm, RegisterForm, EditProfileForm, ChangePasswordForm
from accounts.models import Profile, User


def logout_view(request):
    logout(request)
    return redirect("promotions:all_deals")


def login_view(request):
    template_name = "accounts/login.html"
    context = {"title": "ลงชื่อเข้าใช้"}

    if request.user.is_authenticated:
        logout(request)

    if request.method == "GET":
        form = LoginForm()
        context["form"] = form
        return render(request, template_name, context)

    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_page = request.GET.get("next")
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect("promotions:all_deals")

        context["form"] = form
        form["username"].field.widget.attrs["class"] += " is-invalid"
        form.add_error("username", "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
        messages.add_message(request, messages.ERROR, "ไม่สามารถลงชื่อเข้าใช้ได้")
        return render(request, template_name, context)


def register_view(request):
    template_name = "accounts/register.html"
    context = {"title": "สมัครสมาชิก"}

    if request.user.is_authenticated:
        logout(request)

    if request.method == "GET":
        form = RegisterForm()
        context["form"] = form
        return render(request, template_name, context)

    elif request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name", None)
            surname = form.cleaned_data.get("surname", None)
            tel = form.cleaned_data.get("tel", None)
            email = form.cleaned_data.get("email", None)
            information = form.cleaned_data.get("information", "")
            image = form.cleaned_data.get("image", None)
            birth_date = form.cleaned_data.get("birth_date", None)
            gender = form.cleaned_data.get("gender", None)

            username = form.cleaned_data.get("username", None)
            password = form.cleaned_data.get("password", None)

            new_user = User(username=username)
            new_user.set_password(password)
            new_user.save()

            profile = Profile(
                user=new_user,
                name=name,
                surname=surname,
                image=image,
                tel=tel,
                email=email,
                information=information,
                birth_date=birth_date,
                gender=gender,
            )
            profile.save()

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("promotions:all_deals")

        for field in form.fields:
            if field in ["password", "password2"]:
                continue

            if form[field].errors:
                form[field].field.widget.attrs["class"] += " is-invalid"
            else:
                form[field].field.widget.attrs["class"] += " is-valid"

        if form["password2"].errors or form["password"].errors:
            form["password"].field.widget.attrs["class"] += " is-invalid"
            form["password2"].field.widget.attrs["class"] += " is-invalid"

        context["form"] = form
        messages.add_message(request, messages.ERROR, "กรุณากรอกข้อมูลให้ถูกต้อง")
        return render(request, template_name, context)


@login_required
def profile_view(request):
    template_name = "accounts/profile.html"
    context = {"title": "บัญชี"}

    profile = Profile.objects.filter(user=request.user).first()

    if not profile:
        profile = Profile(user=request.user, information="", genter=Profile.MALE)
        profile.save()

    if request.method == "GET":
        form = EditProfileForm(
            initial={
                "name": profile.name,
                "surname": profile.surname,
                "email": profile.email,
                "tel": profile.tel,
                "information": profile.information,
                "birth_date": profile.birth_date,
                "gender": profile.gender,
                "username": request.user.username,
            }
        )
        context["form"] = form
        return render(request, template_name, context)

    elif request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
        form["username"].initial = request.user.username
        if form.is_valid():
            field_list = [
                "name",
                "surname",
                "tel",
                "email",
                "information",
                "image",
                "birth_date",
                "gender",
            ]
            profile = request.user.profile
            for key in field_list:
                setattr(profile, key, form.cleaned_data.get(key))
            profile.save()
            context["form"] = form
            messages.add_message(request, messages.SUCCESS, "แก้ไขประวัติเรียบร้อยแล้ว")
            return render(request, template_name, context)

        for field in form.fields:
            if form[field].errors:
                form[field].field.widget.attrs["class"] += " is-invalid"
            else:
                form[field].field.widget.attrs["class"] += " is-valid"

        context["form"] = form
        messages.add_message(request, messages.ERROR, "ไม่สามารถแก้ไขประวัติได้")
        return render(request, template_name, context)


@login_required
def change_password_view(request):
    template_name = "accounts/change_password.html"
    context = {"title": "เปลี่ยนรหัสผ่าน"}

    if request.method == "GET":
        form = ChangePasswordForm(initial={"username": request.user.username})
        context["form"] = form
        return render(request, template_name, context)

    elif request.method == "POST":
        form = ChangePasswordForm(request.POST)
        form["username"].initial = request.user.username

        if form.is_valid():
            username = request.user.username
            old_password = form.cleaned_data.get("old_password")
            user = authenticate(request, username=username, password=old_password)

            if user == request.user:
                password = form.cleaned_data.get("password")
                request.user.set_password(password)
                request.user.save()
                logout(request)
                messages.add_message(
                    request, messages.SUCCESS, "เปลี่ยนรหัสผ่านเรียบร้อยแล้ว"
                )
                return redirect("accounts:login")

            else:
                form.add_error("old_password", "รหัสผ่านเก่าไม่ถูกต้อง")

        if form["old_password"].errors:
            form["old_password"].field.widget.attrs["class"] += " is-invalid"

        if form["password2"].errors or form["password"].errors:
            form["password"].field.widget.attrs["class"] += " is-invalid"
            form["password2"].field.widget.attrs["class"] += " is-invalid"

        context["form"] = form
        messages.add_message(request, messages.ERROR, "มีข้อผิดพลาดบางอย่างเกิดขึ้น")
        return render(request, template_name, context)
