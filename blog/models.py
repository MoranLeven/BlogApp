from django.db import models
from django.urls import reverse
# from django.contrib.postgres.fields import JSONField
import uuid
# Create your models here.
class BlogPost(models.Model):
    #column name
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    blog_content = models.TextField()
    image = models.ImageField(upload_to="images/")
    blog_id = models.UUIDField(unique=True,primary_key=True,editable=False,default=uuid.uuid4)
    url = models.URLField()

    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return reverse("home")
    
    #overriding the save method
    # def save(self,*args,**kwargs):
    #     if self.blog_id:
    #         self.blog_id = str(uuid.uuid4())
    #     return super().save(*args,**kwargs)

class VersionPost(models.Model):
    blog = models.OneToOneField(BlogPost,on_delete=models.CASCADE,primary_key=True,to_field='blog_id')
    versions = models.JSONField()
    name = models.CharField(max_length=200)
    
    def save(self,*args,**kwargs):
        if not self.name:
            self.name = self.blog.title
        return super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name


class ReplyPost(models.Model):
    parentId = models.CharField(max_length=50,null=True,blank=True)
    replyId = models.UUIDField(default=uuid.uuid4)
    upvote = models.IntegerField(null=True,blank=True)
    downvote = models.IntegerField(null=True,blank=True)
    childrenReplyId = models.JSONField(default=list)
    replyData = models.TextField()
    hasReply = models.BooleanField(default=False)
    replyDate = models.DateTimeField(auto_now_add=True)
    updateReplyDate = models.DateTimeField(auto_now=True)



