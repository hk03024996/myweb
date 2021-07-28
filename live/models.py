from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class LiveType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name

class Live(models.Model):
    title = models.CharField(max_length=50)
    live_type = models.ForeignKey(LiveType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    readed_num = models.IntegerField(default=0)
    click_nums = models.DateTimeField(auto_now_add=True)
    image = image = models.ImageField(upload_to="live/%Y/%m", verbose_name="首页图片")

    def __str__(self):
        return "<Blog:%s>" % self.title

    class Meta:
        ordering = ['-click_nums']


