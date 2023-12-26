import random

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify, gettext_lazy


class Manager(models.Manager):
    def get_user_by_slug(self, slug):
        try:
            return self.get(slug=slug)
        except ObjectDoesNotExist:
            return None


class Profile(models.Model):
    gender = models.CharField(max_length=10, choices=[('M', gettext_lazy('Male')), ('F', gettext_lazy('Female'))], null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birthday = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    objects = Manager()

    def __str__(self):
        return self.user

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.first_name, self.user.last_name)
        return super(Profile, self).save(*args, **kwargs)


def slugify_user(first_name, last_name):
    """
    Slugify the user name and return the slug
    :param first_name: user first name
    :param last_name: user last name
    :return: slug of user last name and first name if slugified correctly and existed else append  number ot it
    """
    s1 = slugify(first_name)
    s2 = slugify(last_name)
    slug = s1 + s2
    if Profile.objects.get_user_by_slug(slug):
        return slugify_user(slug, random.randint(1, 1000))
    return slug
