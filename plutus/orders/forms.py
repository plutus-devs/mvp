from django import forms


class UploadDeposit(forms.Form):
    image = forms.ImageField(
        label="หลักฐานการโอนเงิน",
        widget=forms.FileInput(attrs={"class": "form-control"}),
    )


class UploadImageForm(UploadDeposit):
    address = forms.CharField(
        label="ที่อยู่จัดส่ง",
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control"})
    )
