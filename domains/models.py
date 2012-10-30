# --*-- coding: utf-8 --*--
from django.contrib import admin
from django.db import models

class DomainsName(models.Model):
    name = models.CharField(max_length=300, db_index=True)

    google_rp = models.SmallIntegerField(default=0)
    google_link = models.IntegerField(default=0)
    google_dir = models.BooleanField(default=False)
    google_serp = models.BooleanField(default=False)

    bing_serp = models.BooleanField(default=False)

    dmoz = models.BooleanField(default=False)

    linking_sites = models.IntegerField(default=0)

    date_valid = models.DateField()

#    age_h_year = models.SmallIntegerField(default=0)
#    age_h_count = models.SmallIntegerField(default=0)

    is_update = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % self.name

#    Creation Date: 24-jun-1997
#s="Creation Date: 24-jun-1997"


class DomainsNameAdmin(admin.ModelAdmin):
    list_display = ['name', 'google_link', 'google_dir', 'dmoz']
admin.site.register(DomainsName, DomainsNameAdmin)

class AuctionHouse(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Название Аукциона')
    file_prefix = models.CharField(max_length=30, verbose_name=u'Префикс файла')
    parser_separator = models.CharField(max_length=10, verbose_name=u'Строка для парсинга')
    domains_number = models.IntegerField(default=0, verbose_name=u'Количество доменов')


class ProxyList(models.Model):
    ip = models.CharField(max_length=50)