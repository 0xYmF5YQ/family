from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import Parents, Children

class FamilyNameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        try:
            user = User.objects.get(username=username)
            if user.is_superuser and user.check_password(password):
                return user
        except User.DoesNotExist:
            pass

        person = Parents.objects.filter(name__iexact=username).first()
        if not person:
            person = Children.objects.filter(name__iexact=username).first()

        if person and person.user:
            year_of_birth = str(person.birth_date.year)
            if password == year_of_birth or person.user.check_password(password):
                return person.user
        
        return None