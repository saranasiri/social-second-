from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    age = models.PositiveSmallIntegerField()


def save_profile(sender, **kwargs):
    if kwargs['created']:
        p1 = profile(user=kwargs['instance'])
        p1.save()


post_save.connect(save_profile, sender=User)


class relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    class META:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.from_user}following {self.to_user}"
