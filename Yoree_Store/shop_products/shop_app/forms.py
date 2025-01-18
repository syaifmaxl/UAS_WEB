from django import forms

class BillingAddressForm(forms.Form):
    name = forms.CharField(label="Full Name", max_length=100, required=True)
    email = forms.EmailField(label="Email Address", required=True)
    mobile_no = forms.CharField(label="Mobile Number", required=True)
    address = forms.CharField(label="Address", widget=forms.Textarea, required=True)
    country = forms.CharField(label="Country", required=True)
    state = forms.CharField(label="State", required=True)
    zip_code = forms.CharField(label="Zip Code", required=True)

class PaymentMethodForm(forms.Form):
    payment_method = forms.ChoiceField(
        label="Payment Method",
        choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')],
        widget=forms.RadioSelect,
        required=True
    )

