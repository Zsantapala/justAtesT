from django.db import models

# Create your models here.
class User(models.Model):
    ''' 用户表 '''
    gender = (
        ('male', '男'),
        ('female', '女'),
    )
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'

class Article(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    text_body = models.TextField(null=True)
    cre_time = models.DateTimeField(auto_now_add=True)
    mod_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.headline
    class Meta:
        ordering = ['cre_time']
        verbose_name = '文章'
        verbose_name_plural = '文章'

class hashID(models.Model):
    u_id = models.ForeignKey(User, on_delete=models.CASCADE)
    UhashID = models.CharField(max_length=128)
    c_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.UhashID
    class Meta:
        ordering = ['c_time']
        verbose_name = 'Hash'
        verbose_name_plural = 'Hash'

