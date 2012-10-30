#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
#sys.path.append('/home/nalog/webapps/django/lib/python2.7/')
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

sys.path.append('/home/vako/django/locum/dropday/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.contrib.auth.models import User
from domains.models import DomainsName, ProxyList
from parser.parser import Parser

#def do_smth():
#    import settings
#    list = Messages.objects.filter(email_sender = False).order_by('id')[:10]
#    for elem in list:
#        elem.email_sender = True
#        elem.save()
#        subject = elem.email_title
#        html_content = render_to_string('news/email.html', locals())
#        text_content = strip_tags(html_content)
#        msg = EmailMultiAlternatives(subject, text_content, settings.SERVER_EMAIL, [elem.email_from])
#        msg.attach_alternative(html_content, "text/html")
#        msg.send()
#    return True


if __name__ == "__main__":
    df = Parser(str=',|0', model=DomainsName)
    df.openFile('/home/vako/django/locum/dropday/media/files/info2.txt')
#    df.get_proxy_list(name_file='/home/vako/django/locum/dropday/media/files/proxy_list.txt', model=ProxyList)
