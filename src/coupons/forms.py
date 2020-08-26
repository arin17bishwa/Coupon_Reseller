from django import forms

from .models import (Coupon,
                     )


class CreateCouponForm(forms.ModelForm):

    class Meta:
        model=Coupon
        fields=[
            'meal',
            'hall',
            'price',
            'sold',
        ]


class UpdateCouponForm(forms.ModelForm):

    class Meta:
        model=Coupon
        fields = [
            'meal',
            'hall',
            'price',
            'sold',
        ]

    def save(self, commit=True):
        coupon=self.instance
        coupon.meal=self.cleaned_data['meal']
        coupon.hall=self.cleaned_data['hall']
        coupon.price=self.cleaned_data['price']
        coupon.sold=self.cleaned_data['sold']

        if commit:
            coupon.save()
        return coupon
