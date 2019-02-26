from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nikename = models.CharField(max_length=16)

    def __str__(self):
        return '<Profile {} for {}>'.format(self.nikename, self.user.username)


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    collection = models.URLField()
    info = models.CharField(max_length=255, null=True)


def get_nikename(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nikename
    else:
        return ''


def get_nikename_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nikename
    else:
        return self.username


def has_nikename(self):
    return Profile.objects.filter(user=self).exists()


User.get_nikename = get_nikename
User.has_nikename = has_nikename
User.get_nikename_or_username = get_nikename_or_username
