# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from cms.forms.widgets import PageSmartLinkWidget
from django.contrib import admin
from django.contrib.sites.models import Site
from django.forms import ModelForm, HiddenInput
from django.utils.translation import get_language

from .models import Redirect


class RedirectForm(ModelForm):
    class Meta:
        model = Redirect
        fields = ['site', 'old_path', 'new_path', 'response_code']

    def __init__(self, *args, **kwargs):
        super(RedirectForm, self).__init__(*args, **kwargs)
        widget = PageSmartLinkWidget(ajax_view='admin:cms_page_get_published_pagelist')
        widget.language = get_language()
        self.fields['site'].widget = HiddenInput()
        self.fields['site'].initial = Site.objects.get_current().pk
        self.fields['old_path'].widget = widget
        self.fields['new_path'].widget = widget


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'response_code')
    list_filter = ('site',)
    search_fields = ('old_path', 'new_path')
    radio_fields = {'site': admin.VERTICAL}
    form = RedirectForm
