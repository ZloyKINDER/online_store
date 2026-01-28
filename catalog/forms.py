from django import forms
from .models import Category, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "category", "purchase_price", "image"]

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

