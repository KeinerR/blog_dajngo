from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


# Create your models here.
class SoftDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()



        
class Permission(SoftDeleteModel):
    codename = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
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

class File(SoftDeleteModel):
    # La ruta al archivo real (imagen, PDF, etc.)
    file = models.FileField(upload_to='generic_files/')
    description = models.CharField(max_length=255, blank=True)
    published_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey( User,on_delete=models.SET_NULL, null=True ,related_name='file')
    
    # 1. Foreign Key al ContentType
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    
    # 2. ID del objeto padre
    object_id = models.PositiveIntegerField()

    # 3. La Generic Foreign Key (es una propiedad, no se crea como una columna en la BD)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        # Esto asegura que no puedas tener dos archivos idénticos para el mismo objeto padre
        unique_together = (('content_type', 'object_id', 'file'),)
        db_table = "File"    
        db_table_comment = "Files"        

class Post(SoftDeleteModel):
    title = models.CharField(max_length=255, blank=False , null=False)
    content = models.TextField( blank=False , null=False)  
    author = models.ForeignKey( User,on_delete=models.CASCADE ,related_name='post')
    published_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=255, unique=True)
    files = GenericRelation(File, related_query_name='post_files') # 🚨 Usar cadena 'File' o 'app_name.File'    
    
    class Meta:
        db_table = 'Post'
        db_table_comment = 'Posts'


class Comment(SoftDeleteModel):
    content = models.TextField( blank=False , null=False)
    author = models.ForeignKey( User,on_delete=models.CASCADE,related_name='comments')
    published_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey( Post,on_delete=models.CASCADE,related_name='comments')
    parent =  models.ForeignKey( 'self',on_delete=models.CASCADE,null=True, blank=True,related_name='replies')  
    files = GenericRelation(File, related_query_name='comment_files')
    
    class Meta:
        db_table = 'Comment'
        db_table_comment = 'Comments'
            
