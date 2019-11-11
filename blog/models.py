from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)#CharField 指定了分类名 name 的数据类型，CharField 是字符型
    
    class Meta:
        verbose_name='分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    '''
    django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    当然 django 还为我们提供了多种其它的数据类型，如日期时间类型 DateTimeField、整数类型 IntegerField 等等。
    django 内置的全部类型可查看文档：
    https://docs.djangoproject.com/en/2.2/ref/models/fields/#field-types
    '''
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name='标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField('标题',max_length=70)#标题
    body = models.TextField('正文')#正文，大段文本用textfield
    created_time = models.DateTimeField('创建时间',default=timezone.now)#时间字段用datefield
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField('摘要',max_length=200,blank=True)#摘要，blank=True代表允许空格
    Category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE)#ForeignKey表示一对多
    tags = models.ManyToManyField(Tag,verbose_name='标签',blank=True)#多对多
    author = models.ForeignKey(User,verbose_name='作者',on_delete=models.CASCADE)
    
    def save(self,*args,**kwargs):
        self.modified_time= timezone.now()
        super().save(*args,**kwargs)

    class Meta:
        verbose_name='文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})