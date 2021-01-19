from django import forms
from foodapp.models import Admin,Food,Cust,Cart,Order

class FoodForm(forms.ModelForm):
	class Meta:
		model = Food
		fields  = "__all__"
		
class CustForm(forms.ModelForm):
	class Meta:
		model = Cust
		fields  = "__all__"
		
class AdminForm(forms.ModelForm):
	class Meta:
		model = Admin
		fields  = "__all__"		
		
class CartForm(forms.ModelForm):
	class Meta:
		model = Cart
		fields  = "__all__"		
		
class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields  = "__all__"		
