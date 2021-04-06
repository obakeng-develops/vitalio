# Django
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, Select, Textarea

# Models
from .models import Assessment

class AssessmentFeelingForm(ModelForm):

    class Meta:
        model = Assessment
        fields = ['feeling_today']

        widgets = {
            'feeling_today': Select(attrs={'class': 'w-25'})
        }
    
    def __init__(self, *args, **kwargs):
        super(AssessmentFeelingForm, self).__init__( *args, **kwargs )
        self.fields['feeling_today'].label = False

class DailyLifeAssessmentForm(ModelForm):

    class Meta:
        model = Assessment
        fields = ['daily_life_feeling']

        widgets = {
            'daily_life_feeling': Select(attrs={'class': 'w-25'})
        }
    
    def __init__(self, *args, **kwargs):
        super(DailyLifeAssessmentForm, self).__init__( *args, **kwargs )
        self.fields['daily_life_feeling'].label = False

class FocusAssessmentForm(ModelForm):

    class Meta:
        model = Assessment
        fields = ['focus_area']

        widgets = {
            'focus_area': Select(attrs={'class': 'w-25'})
        }
    
    def __init__(self, *args, **kwargs):
        super(FocusAssessmentForm, self).__init__( *args, **kwargs )
        self.fields['focus_area'].label = False

class ExpectationAssessmentForm(ModelForm):

    class Meta:
        model = Assessment
        fields = ['expectation']

        widgets = {
            'expectation': Textarea(attrs={'cols': 10, 'rows': 8, 'class': 'shadow'})
        }
    
    def __init__(self, *args, **kwargs):
        super(ExpectationAssessmentForm, self).__init__( *args, **kwargs )
        self.fields['expectation'].label = False