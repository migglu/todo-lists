# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListUser',
            fields=[
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(primary_key=True, serialize=False, max_length=254)),
                ('groups', models.ManyToManyField(related_query_name='user', verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', to='auth.Permission', related_name='user_set')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
