from django import forms
from ckeditor.widgets import CKEditorWidget
from brands.models import Brand
from promotions.models import Category, PromotionType, Promotion


class DatalistInput(forms.widgets.Select):
    input_type = "text"
    template_name = "promotions/datalist.html"

    def format_value(self, value):
        return value if value else ""


class CreatePromotionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreatePromotionForm, self).__init__(*args, **kwargs)
        self.fields["promotion_type"].widget = DatalistInput(
            attrs={"class": "form-control"},
            choices=[(pt.id, pt.name) for pt in PromotionType.objects.all()],
        )

    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        empty_label=None,
        label="แบรนด์",
        widget=forms.Select(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        ),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label=None,
        label="ประเภทสินค้า",
        widget=forms.Select(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        ),
    )
    promotion_type = forms.CharField(
        label="ประเภทโปรโมชั่น",
        widget=None,
    )

    type = forms.ChoiceField(
        label="ส่วนลดโดย",
        choices=Promotion.PROMOTION_TYPE_CHOICES,
        widget=forms.Select(
            attrs={
                "class": "form-control selectpicker",
                "data-live-search": "true",
            }
        ),
    )

    name = forms.CharField(
        label="ชื่อ",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    image = forms.ImageField(
        label="รูปปก (ไม่จำเป็น)",
        widget=forms.FileInput(attrs={"class": "form-control"}),
        required=False,
    )
    url = forms.URLField(
        label="ลิ้งค์เว็บไซต์",
        widget=forms.URLInput(attrs={"class": "form-control"}),
    )
    max_member = forms.IntegerField(
        label="จำนวนที่รับสมัคร",
        min_value=1,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=False,
    )

    close_at = forms.DateTimeField(
        label="วันสิ้นสุด (ค.ศ.)",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "form-control"}
        ),
    )
    description = forms.CharField(
        label="ข้อมูลเพิ่มเติม",
        widget=CKEditorWidget(
            config_name="awesome_ckeditor",
        ),
        required=False,
    )
    deposit_percent = forms.FloatField(
        label="มัดจำขั้นต่ำ (30%)",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "30",
                "max": "100",
                "value": "30",
            }
        ),
    )

    threshold = forms.FloatField(
        label="ราคาคั่น",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
        required=False,
    )
