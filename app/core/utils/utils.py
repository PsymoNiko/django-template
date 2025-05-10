import re
from rest_framework import serializers
import jdatetime

def is_telephone_number_invalid(telephone_number):
    if telephone_number == None:
        return True
    elif re.search(r'\b0\d{2,3}\d{8}\b', telephone_number):
        return False
    else:
        return True



class JalaliDateField(serializers.ReadOnlyField):
    def to_representation(self, value):
        return jdatetime.date.fromgregorian(date=value).strftime("%Y-%m-%d")


def convert_datetime_to_jalali_date(value):
    jalali_date = jdatetime.date.fromgregorian(date=value.date())
    return jalali_date


def convert_date_to_jalali_date(value):
    jalali_date = jdatetime.date.fromgregorian(date=value)
    return jalali_date


def convert_date_to_jalali_date_serializable(value):
    jalali_date = jdatetime.date.fromgregorian(date=value)
    return jalali_date.strftime('%m/%d')
