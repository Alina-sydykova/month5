
from datetime import date, datetime
from django.core.exceptions import ValidationError

MSG_UNDER_18 = "Вам должно быть 18 лет, чтобы создать продукт."

def _parse_birthday(value):
    
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str):
       
        try:
            return date.fromisoformat(value)
        except ValueError:
            
            try:
                return datetime.fromisoformat(value).date()
            except ValueError:
                return None
    return None

def validate_age_18(birthday_value):
   
    bdate = _parse_birthday(birthday_value)
    if not bdate:
        raise ValidationError(MSG_UNDER_18)

    today = date.today()
    years = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
    if years < 18:
        raise ValidationError(MSG_UNDER_18)
    return True
