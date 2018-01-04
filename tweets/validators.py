from django.core.exceptions import ValidationError



def validate_content(value):
  content = value
  if content == "abc":
    raise ValidationError("content can not abc")
  return value