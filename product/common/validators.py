from datetime import date
from django.core.exceptions import ValidationError

def validate_age_18(birthday):
    if not birthday:
        raise ValidationError("Поле даты рождения обязательно.")

    today = date.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    if age < 18:
        raise ValidationError("Вам должно быть 18 лет, чтобы создать продукт.")
