from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    title = models.CharField(verbose_name=_("title"),max_length=50)
    description = models.TextField(verbose_name=_("description"),blank=True)
    avatar = models.ImageField(verbose_name=_("avatar"),blank=True,upload_to='categories')
    is_enable = models.BooleanField(verbose_name=_("is enable"),default=True)
    parent = models.ForeignKey('self',verbose_name=_("parent"),blank=True,null=True, on_delete= models.CASCADE)
    create_time = models.DateTimeField(verbose_name=_("create time"),auto_now_add=True)
    update_time = models.DateTimeField(verbose_name=_("update time"),auto_now=True)
    
    class Meta:
        db_table = "categories"
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        
    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=100)
    #user = models.ForeignKey(User, on_delete= models.CASCADE)
    price = models.BigIntegerField(verbose_name=_('price'))
    caption = models.TextField(verbose_name=_('caption'),blank=True,max_length=1024,null=True)
    is_active = models.BooleanField(default=True,null=True)
    is_enable = models.BooleanField(default=True,null=True)
    uniqe_code = models.IntegerField(verbose_name=_('uniqe_code'),unique=True)
    categories = models.ManyToManyField('Category',verbose_name=_("categories"),blank=True)
    create_time = models.DateTimeField(
        verbose_name=_("create time"), auto_now_add=True)
    update_time = models.DateTimeField(
        verbose_name=_("update time"), auto_now=True)
    
    class Meta:
        db_table = 'Posts'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
    
    def __str__(self):
        return self.title

class Post_File(models.Model):
    FILE_VIDEO = 1
    FILE_IMG = 2
    FILE_TYPES = (
        (FILE_VIDEO,_('video')),
        (FILE_IMG,_('image'))
    )
    title = models.CharField(_("title"),max_length=50)
    file_type =models.PositiveSmallIntegerField(_("file type"), choices=FILE_TYPES)
    fil = models.FileField(_("file"),upload_to="media/%Y/%m/%d/")
    post = models.ForeignKey('Product',verbose_name=_("Product"),related_name='files', on_delete=models.CASCADE)
    is_enable = models.BooleanField(_("is enable"),default=True)
    create_time = models.DateTimeField(_("create time"),auto_now_add=True)
    update_time = models.DateTimeField(_("update time"),auto_now=True)
    
    class Meta:
        db_table = "files"
        verbose_name = _("file")
        verbose_name_plural = _("files")
        
    def __str__(self):
        return self.title    
    
class Comment(models.Model):
    #user = models.ForeignKey(to=User, on_delete= models.PROTECT)
    Product = models.ForeignKey(to=Product,related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=2048)
    is_approved = models.BooleanField(default=True)
    create_time = models.DateTimeField(_("create time"),auto_now_add=True)
    update_time = models.DateTimeField(_("update time"),auto_now=True)
    
    class Meta:
        db_table = "Comments"
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")