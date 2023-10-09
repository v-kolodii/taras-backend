""" Models Classes Appeal """
from django.db.models import (Model, CharField, TextField, DateTimeField, 
                              ForeignKey, IntegerField, IntegerChoices, CASCADE, SET_NULL)
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from accounts.models import User

class Category(Model):
    """Class representing an Appeals"""
    name = CharField(max_length=200, unique=True)

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('posts')

class Appeal(Model):
    """Class representing a Appeals"""
    class AppealStatus(IntegerChoices):
        """Class representing an Appeals status choice"""
        NEW = 1
        ON_MODERATION = 2
        ASSIGNED = 3
        COMPLETED = 4
        DELETED = 5

    title = CharField(_("Appeals title"), max_length=255, blank=True)
    text = TextField(_("Appeals text"), blank=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    category = ForeignKey(Category, on_delete=CASCADE)
    creator = ForeignKey(User, on_delete=CASCADE, related_name='appeal_creators_set')
    assigned_to = ForeignKey(User, on_delete=SET_NULL, blank=True, null=True, related_name='appeal_assigned_set')
    app_status = IntegerField(_("Appeal status"), choices=AppealStatus.choices, default=AppealStatus.NEW)
    
    class Meta:
        """Class representing a Appeals Meta"""
        ordering = ['updated_at']
    
    def __str__(self):
        return str(self.title)