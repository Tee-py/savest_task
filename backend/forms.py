from django import forms



class MailForm(forms.Form):
    subject = forms.CharField(
        required=True,
        max_length=200
    )
    From = forms.EmailField(max_length=200,required=True)
    body = forms.CharField(
        max_length=5000,
        required=True,
        widget=forms.Textarea(),
        help_text='Type Message Body Here!'
    )

    def clean(self):
        cleaned_data = super(MailForm, self).clean()
        return cleaned_data


