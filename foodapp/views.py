from django.shortcuts import render, redirect
from django.db import connection, transaction
from foodapp.forms import FoodForm,CustForm,AdminForm,CartForm,OrderForm
from foodapp.models import Food,Cust,Admin,Cart,Order
import datetime

cursor = connection.cursor()



# ---------------------------------------This function renders the index page-----------------------------.
def foodapp(request):
	return render(request,'index.html')



#------------------------ This function allows an admin to add food details and redirects to the food list-----------------------------------
def addfood(request):
	if request.method=="POST":
		form = FoodForm(request.POST,request.FILES)
		if form.is_valid():
			try:
				form.save()
				return redirect("/allfood")
			except:
				return render(request,"error.html")
	else :
		form = FoodForm()
	return render(request,'addfood.html',{'form':form})
	


# -------------------------This function retrieves and displays the list of food items--------------------------
def showfood(request):
	foods = Food.objects.all()
	return render(request,'foodlist.html',{'foodlist':foods})
	

#-----------------------This function allows an admin to delete a specific food item and redirects to the food list.---------------
def deletefood(request,FoodId):
	foods = Food.objects.get(FoodId=FoodId)
	foods.delete()
	return redirect("/allfood")


#------------------This function retrieves a specific food item for editing.-----------------------------
def getfood(request,FoodId):
	foods = Food.objects.get(FoodId=FoodId)
	return render(request,'updatefood.html',{'f':foods})


#------------------------This function allows an admin to update the details of a specific food item and redirects to the food list.------------------------
def updatefood(request,FoodId):
	foods = Food.objects.get(FoodId=FoodId)
	form = FoodForm(request.POST,request.FILES,instance=foods)
	if form.is_valid():
		form.save()
		return redirect("/allfood")
	return render(request,'updatefood.html',{'f':foods})
	
#-----------------This function allows a user to register and redirects to the login page.----------------------
def addcust(request):
	if request.method=="POST":
		form = CustForm(request.POST)
		if form.is_valid():
			try:
				form.save()
				return redirect("/login")
			except:
				return render(request,"error.html")
	else :
		form = CustForm()
	return render(request,'addcust.html',{'form':form})



#------------------------This function retrieves and displays the list of customers.-------------------------
def showcust(request):
	custs = Cust.objects.all()
	return render(request,'custlist.html',{'custlist':custs})


#--------------This function allows an admin to delete a specific customer and redirects to the customer list.-----------------------
def deletecust(request,CustId):
	custs = Cust.objects.get(CustId=CustId)
	custs.delete()
	return redirect("/allcustomer")
	

#----------This function retrieves and displays the details of a logged-in customer for editing.-------------------
def getcust(request):
	print(request.session['CustId'])
	for c in Cust.objects.raw('Select * from FP_Cust where CustEmail="%s"'%request.session['CustId']):
		custs=c
	return render(request,'updatecust.html',{'c':custs})
	
#--------This function allows a user to update their details and logs them out for security purposes.--------------------
def updatecust(request,CustId):
	custs = Cust.objects.get(CustId=CustId)
	form = CustForm(request.POST,instance=custs)
	if form.is_valid():
		form.save()
		session_keys = list(request.session.keys())
		for key in session_keys:
			del request.session[key]
		return redirect("/login")
	return render(request,'updatecust.html',{'c':custs})
	
	
#------------------This function renders the login page------------------------
def login(request):
	return render(request,'login.html')
	

#------------------This function handles user and admin login and sets session variables accordingly.------------------
def doLogin(request):
	if request.method=="POST":
		uid = request.POST.get('userId','')
		upass = request.POST.get('userpass','')
		utype = request.POST.get('type','')
		
		if utype == "Admin":
			for a in Admin.objects.raw('Select * from FP_Admin where AdminId="%s" and AdminPass="%s"'%(uid,upass)):
				if a.AdminId==uid:
					request.session['AdminId']=uid
					return render(request,"index.html",{'success':'Welcome '+a.AdminId})
			else:
				return render(request,"login.html",{'failure':'Incorrect login details'})
					
		if utype == "User":
			for a in Cust.objects.raw('Select * from FP_Cust where CustEmail="%s" and CustPass="%s"'%(uid,upass)):
				if a.CustEmail==uid:
					request.session['CustId']=uid
					return render(request,"index.html",{'success':'Welcome '+a.CustEmail})
			else:
				return render(request,"login.html",{'failure':'Incorrect login details'})


#-------------This function logs out the user or admin by clearing session variables.---------------------------			
def doLogout(request):
	key_session = list(request.session.keys())
	for key in key_session:
		del request.session[key]
	return render(request,'index.html',{'success':'Logged out successfully'})
	

#-----------This function allows a user to add food items to their cart.-----------------------
def addcart(request,FoodId):
	sql = ' Insert into FP_Cart(CustEmail,FoodId,FoodQuant) values("%s","%d","%d")'%(request.session['CustId'],FoodId,1)
	i=cursor.execute(sql)
	transaction.commit()
	return redirect('/allfood')
	

#-----------------This function allows a user to remove items from their cart and redirects to the cart page.-----------------
def delcart(request,CartId):
	cart = Cart.objects.get(CartId=CartId)
	cart.delete()
	return redirect("/allcart")

#---------------------This function retrieves and displays the list of items in the user's cart.------------------------	
def showcart(request):
	cart=Cart.objects.raw('Select CartId,FoodName,FoodPrice,FoodQuant,FoodImage from FP_Food as f inner join FP_Cart as c on f.FoodId=c.FoodId where c.CustEmail="%s"'%request.session['CustId'])
	transaction.commit()
	return render(request,"cartlist.html",{'cartlist':cart})


#------------------------This function renders the password update page.---------------------------------------
def updatepasswd(request):
	return render(request,'updatepasswd.html')


#-----------------This function handles the process of changing the password and logs the user out for security reasons.--------------------------	
def changepass(request):
	if request.method == "POST":
		aid=request.session['AdminId']
		opss=request.POST.get('OLDPass','')
		newpss=request.POST.get('NEWPass','')
		cnewpss=request.POST.get('CONFPass','')
		for a in Admin.objects.raw('select * from FP_Admin where AdminId="%s" and AdminPass="%s"'%(aid,opss)):
			if a.AdminId == aid:
				sql = 'update FP_Admin set AdminPass="%s" where AdminId="%s"' %(newpss,request.session['AdminId'])
				i=cursor.execute(sql)
				transaction.commit()
				session_keys = list(request.session.keys())
				for key in session_keys:
					del request.session[key]
				return redirect("/login")
		else:
			return render(request,'updatepasswd.html',{'failure':'Invalid attempt.'})


#-----------------------This function allows a user to place an order and clears the cart.----------------------------
def placeorder(request):
        if request.method=="POST":
                price=request.POST.getlist('FoodPrice','')
                q=request.POST.getlist('FoodQuant','')
                total=0.0
                for i in range(len(price)):
                    total=total+float(price[i])*float(q[i])
                today = datetime.datetime.now()
                sql = 'insert into FP_Order(CustEmail,OrderDate,TotalBill) values ("%s","%s","%f")' %(request.session['CustId'],today,total)
                i=cursor.execute(sql)
                transaction.commit()
                sql1= 'select * from FP_Order where CustEmail="%s" and OrderDate="%s"'%(request.session['CustId'],today)
                sql = 'delete from FP_Cart where CustEmail="%s"' %(request.session['CustId'])
                i=cursor.execute(sql)
                transaction.commit()
                
                od=Order()
                
                for o in Order.objects.raw(sql1):
                        if o.CustEmail==request.session['CustId']:
                                od=str(o.OrderId)
                                return render(request,'index.html',{'success':'Order placed sucessfully!!!'+str(o.OrderId)})
        else:
        	pass


#------------------------This function retrieves and displays a list of orders.----------------------------
def getorder(request):
	orders = Order.objects.all()
	return render(request,'orderlist.html',{'orderlist':orders})
#--------------------This function updates the quantity of items in the cart.-------------------------
def updateQNT(request,s):
	print(s)
	ind=s.index('@')
	cartId=int(s[:ind])
	qt=int(s[ind+1:])
	sql="update FP_Cart set FoodQuant='%d' where CartId='%d'"%(qt,cartId)
	i=cursor.execute(sql)
	transaction.commit()
 
