import datetime
from django.forms import ModelForm, DateInput
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from catalog.models import BookInstance


class RenewBookForm(ModelForm):
    def clean_due(self):
        data = self.cleaned_data['due']

        # Check if date isn't set in the past.
        if data < datetime.date.today():
            raise ValidationError(
                _('Date cannot be set in the past.'), code='date_before_today')

        # Check if date is within the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Date cannot be set more than 4 weeks ahead.'), code='date_too_far')

        return data

    class Meta:
        model = BookInstance
        fields = ['due']
        labels = {'due': _('New renewal date')}
        help_texts = {
            'due': _('Enter a date between now and 4 weeks (default 3).')}
        widgets = {'due': DateInput(attrs={'type': 'date'})}
