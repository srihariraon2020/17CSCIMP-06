from django.forms import Form, CharField, PasswordInput, FileField, IntegerField, FloatField


class DataForm(Form):

    District_Name = IntegerField()
    Season = IntegerField()
    Area = FloatField()
    temperature = FloatField()
    humidity = FloatField()
    ph = FloatField()
    rainfall = FloatField()