from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    slug = models.SlugField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} , {self.body[:5]}'

    def get_absolute_url(self):
        return reverse('post:post_detail', args=[self.created.year, self.created.month, self.created.day, self.slug])

    def likes_count(self):
        return self.pvote.count()

    def user_can_like(self, user):
        user_like = user.uvote.all()
        qs = user_like.filter(post=self)
        if qs.exists():
            return True
        return False


class comment(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(post , on_delete=models.CASCADE)
    reply= models.ForeignKey('self',on_delete= models.CASCADE , null=True,blank=True,related_name='rcomment')
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}_{self.body[:30]}'



class vote (models.Model):
    post = models.ForeignKey(post,on_delete=models.CASCADE , related_name = 'pvote')
    user = models.ForeignKey(User,on_delete=models.CASCADE , related_name = 'uvote')

    def __str__(self):
        return f'{self.user} liked {self.post}'