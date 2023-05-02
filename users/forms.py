from django.forms import modelform_factory

from .models import User


login_form = modelform_factory(User, fields=['username', 'password'])
