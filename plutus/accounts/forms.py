from django import forms
from accounts.models import Profile, User


class LoginForm(forms.Form):

    username = forms.CharField(
        label="ชื่อผู้ใช้",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
                   }
        ),
    )

    password = forms.CharField(
        label="รหัสผ่าน",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class RegisterForm(forms.Form):
    error_messages = {
        "username_exists": "ชื่อผู้ใช้นี้มีอยู่แล้ว",
        "password_mismatch": "รหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน",
    }

    image = forms.ImageField(
        label="รูปโปรไฟล์",
        widget=forms.FileInput(attrs={"class": "form-control"}),
        required=False,
    )

    name = forms.CharField(
        label="ชื่อ",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    surname = forms.CharField(
        label="นามสกุล",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="อีเมล",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    tel = forms.CharField(
        label="เบอร์ติดต่อ",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    information = forms.CharField(
        label="ข้อมูลเพิ่มเติม",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
        required=False,
    )

    birth_date = forms.DateField(
        label="วันเกิด (ค.ศ.)",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    gender = forms.ChoiceField(
        choices=Profile.GENDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    username = forms.CharField(
        label="ชื่อผู้ใช้",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="รหัสผ่าน",
        min_length=6,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="รหัสผ่านยืนยัน",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        user = User.objects.filter(username=username).first()
        if user:
            self.add_error("username", self.error_messages["username_exists"])
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password", None)
        password2 = cleaned_data.get("password2", None)
        if password is not None and password != password2:
            self.add_error("password2", self.error_messages["password_mismatch"])
        return cleaned_data


class EditProfileForm(forms.Form):

    image = forms.ImageField(
        label="รูปโปรไฟล์",
        widget=forms.FileInput(attrs={"class": "form-control"}),
        required=False,
    )

    name = forms.CharField(
        label="ชื่อ",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    surname = forms.CharField(
        label="นามสกุล",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="อีเมล",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    tel = forms.CharField(
        label="เบอร์ติดต่อ",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    information = forms.CharField(
        label="ข้อมูลเพิ่มเติม",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
        required=False,
    )

    birth_date = forms.DateField(
        label="วันเกิด (ค.ศ.)",
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
    )
    gender = forms.ChoiceField(
        choices=Profile.GENDER_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    username = forms.CharField(
        label="ชื่อผู้ใช้",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
        disabled=True,
    )


class ChangePasswordForm(forms.Form):

    error_messages = {
        "password_mismatch": "รหัสผ่านและยืนยันรหัสผ่านไม่ตรงกัน",
    }

    username = forms.CharField(
        label="ชื่อผู้ใช้",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
        disabled=True,
    )

    old_password = forms.CharField(
        label="รหัสผ่านเก่า",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "กรุณากรอกรหัสผ่านเก่าของคุณ",
                "class": "form-control",
            }
        ),
    )

    password = forms.CharField(
        label="รหัสผ่านใหม่",
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "กรุณากรอกรหัสผ่านใหม่ของคุณ",
                "class": "form-control",
            }
        ),
    )
    password2 = forms.CharField(
        label="รหัสผ่านยืนยัน",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "กรุณากรอกรหัสผ่านใหม่ของคุณอีกครั้ง",
                "class": "form-control",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password", None)
        password2 = cleaned_data.get("password2", None)
        if password is not None and password != password2:
            self.add_error("password2", self.error_messages["password_mismatch"])
        return cleaned_data
