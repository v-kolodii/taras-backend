'''User model'''
from django.db.models import (EmailField, BooleanField, CharField, DateTimeField)
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    """User manager"""
    use_in_migrations = True

    def create_user(self, email, password=None, phone=None, name=None, second_name=None, 
                     is_staff=None, is_admin=None, is_moderator=False, is_active=True):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError("The email is required!")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.phone = phone
        user.second_name = second_name
        user.staff = is_staff
        user.admin = is_admin
        user.moderator = is_moderator
        user.is_active = is_active
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, name=None):
        ''' Create superuser '''
        return self.create_user(email, password=password, name=name, is_staff=True, is_admin=True)
    
    def create_staffuser(self, email, password=None, name=None):
        ''' Create staffuser '''
        return self.create_user(email, password=password, name=name, is_staff=True, is_admin=False)
    
    def create_moderator(self, email, password=None, name=None):
        ''' Create moderator '''
        return self.create_user(email, password=password, name=name, is_staff=True, is_moderator=True)


class User(AbstractBaseUser):
    ''' Class representing a User '''
    email = EmailField(unique=True, max_length=255)
    phone = CharField(verbose_name='phone', max_length=30, null=True)
    name = CharField(max_length=255, blank=True, null=True)
    second_name = CharField(max_length=255, blank=True, null=True)
    staff = BooleanField(default=False)
    admin = BooleanField(default=False)
    moderator = BooleanField(default=False)
    is_active = BooleanField(default=True)
    timestamp = DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        '''return email for str interprete'''
        return  str(self.email)
    
    def get_full_name(self):
        '''return full name or email'''
        return self.name + ' ' + self.second_name if self.name and self.second_name else self.email
    
    def has_perm(self, perm, obj=None):
        '''app permission'''
        return True
    
    def has_module_perms(self, app_label):
        '''module permission'''
        return True

    @property
    def is_admin(self):
        """Check if admin prop"""
        return self.admin
    
    @property
    def is_staff(self):
        """Check if staff prop"""
        return True if self.admin else self.staff

    def save(self, *args, **kwargs):
        print(self.password)
        if not self.id and not self.staff and not self.admin:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
