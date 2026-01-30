from django import forms
from .models import Category, Product
from django.core.exceptions import ValidationError

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите наименование"
        })

        self.fields["description"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите описание"
        })



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "purchase_price", "image"]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите наименование"
        })

        self.fields["description"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите описание"
        })

        self.fields["category"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Выберите категорию"
        })

        self.fields["purchase_price"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Введите стоимость"
        })

        self.fields["image"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Загрузите изображение"
        })

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data.get("purchase_price")

        if purchase_price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return purchase_price

    def clean(self):
        ban_words = ["казино", "биржа", "обман", "криптовалюта", "дешево",
                     "полиция", "крипта", "бесплатно", "радар"]
        cleaned_date = super().clean()
        name = cleaned_date.get("name")
        description = cleaned_date.get("description")

        if any(word in name.lower() for word in ban_words):
            self.add_error("name","Использованны запрещённые слова")

        if any(word in description.lower() for word in ban_words):
            self.add_error("description","Использованны запрещённые слова")

