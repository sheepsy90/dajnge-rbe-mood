from __future__ import unicode_literals

from django.core.exceptions import ValidationError


def validated_answer_possibilities(parameters):
    if not parameters:
        raise ValidationError('Must be a given value')

    if not isinstance(parameters, dict):
        raise ValidationError('Parameter must be a dictionary')

    if len(parameters.items()) not in [2, 4, 5]:
        raise ValidationError('Parameter dict length needs to be in [2, 4, 5]')