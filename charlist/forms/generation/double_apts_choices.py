# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form


class DoubleAptsChoiceForm(Form):
    apt_choice = forms.ChoiceField(label=u'Первая склонность')
    apt_choice2 = forms.ChoiceField(label=u'Вторая склонность')

    def is_valid(self):
        return super().is_valid() and (self.apt_choice != self.apt_choice2)
