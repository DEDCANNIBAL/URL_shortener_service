from django.db import models
from django.conf import settings


class ShortUrl(models.Model):
    short_url = models.CharField(max_length=6, primary_key=True, verbose_name='Short URL')
    origin_url = models.CharField(max_length=2100, verbose_name='Origin URL')
    click_counter = models.BigIntegerField(verbose_name='All clicks', default=0)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date of creation')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True
    )
