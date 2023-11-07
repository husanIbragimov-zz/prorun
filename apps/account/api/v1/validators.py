from rest_framework.exceptions import ValidationError
import os, re


def validate_file_size(value):
    filesize = value.size
    if filesize > 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 30MB")
    return value


def is_word_latin(word):
    latin_pattern = re.compile(r'^[a-zA-Z]+$')

    if latin_pattern.match(word):
        return True
    return False
