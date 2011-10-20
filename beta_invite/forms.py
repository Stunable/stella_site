"""
Form for email sign up. 
"""

from django import Forms

class SignupForm(forms.Form):
    """
    Form for signing up to the site Beta launch. 

    """
    email = forms.EmailField()
