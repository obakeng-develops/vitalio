# Django
from django.forms import ModelForm, DateInput, TimeInput

# Models
from .models import Schedule, Booking

class ScheduleForm(ModelForm):
  class Meta:
    model = Schedule
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
        'day': DateInput(attrs={'type': 'date'}, format="%Y-%m-%d"),
        'start_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        'end_time': TimeInput(attrs={'type': 'time'}, format='%H:%M'),
    }
    fields = '__all__'
    exclude = ['account', 'isBooked']

  def __init__(self, *args, **kwargs):
    super(ScheduleForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['day'].input_formats = ('%Y-%m-%d',)
    self.fields['start_time'].input_formats = ('%H:%M',)
    self.fields['end_time'].input_formats = ('%H:%M',)

class BookingForm(ModelForm):
  class Meta:
    model = Booking
    fields = '__all__'