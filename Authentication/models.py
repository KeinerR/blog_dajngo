from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
 

# Create your models here.

class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        abstract = True
    def delete(self,*args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()
    
    def restore(self):
        self.deleted_at = None
        self.save()
 
class Permission(SoftDeleteModel):
    codename = models.CharField(max_length = 100, unique= True)
    name = models.CharField(max_length=225, blank=False, null=False)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='permissions'
    )

    class Meta:
        db_table = "Permission"    
        db_table_comment = "Permissions"
        unique_together = [['codename', 'content_type']]
        
    def __str__(self):
        return f"{self.content_type.app_label}.{self.codename}"

class Role(SoftDeleteModel):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')
    
    class Meta:
        db_table = "Role"    
        db_table_comment = "Roles"

    def __str__(self):
        return self.name
   
class User(AbstractUser,SoftDeleteModel):
    email = models.EmailField(max_length=50, unique=True)
    roles = models.ManyToManyField(Role, related_name='users')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = "User"    
        db_table_comment = "Users"
