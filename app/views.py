# request.session['key'] = value                     # syntax (session mai data stor karane ke liye)
# EX. request.session['email'] = uid.email            # Session me email(data) store kar rahe hai.

# del request.session['key']                          # syntax (session  ka data delete karan)
# EX. del request.session['email']                      # Ex (session  ka data delete karane ka.)

# value = request.session.get('key', 'default_value')  # session ke data ko gate karane ke liye(data retvieve)

# request.session.flush()               # sare session data ko delete (log-out jaisi sisvation pe) use kiya jata hai





from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.





def index(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session["email"])
        con = {"uid":uid}
        return render(request,"index.html",con)
    else:
        return render(request,"login.html")
    
    
def error(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session["email"])
        con = {"uid":uid}
        return render(request,"error.html",con)
    else:
        return render(request,"login.html")
    
from django.db.models import Q
def shop(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session["email"])
        cid = Categories.objects.all()
        price_show = Price.objects.all()
        sorting = request.GET.get("sort")
        price = request.GET.get("price")
        category = request.GET.get("category")
        additional_filter = request.GET.getlist('Additional_filter')
        cart_item = Add_to_cart.objects.filter(user_id=uid)
        wishlist_items= Add_to_Wishlist.objects.filter(user_id=uid)

        # Initial query
        products = Product.objects.all()

        # Category filtering
        if category:
            products = products.filter(cat_id=category)

        # Price filtering
        if price:
            products = products.filter(price_id=price)

        # Additional filtering
        if additional_filter:
            products = products.filter(Additional_filter__in=additional_filter)

        # Sorting
        if sorting == "lth":
            products = products.order_by("price")
        elif sorting == "htl":
            products = products.order_by("-price")
        elif sorting == "atz":
            products = products.order_by("name")
        elif sorting == "zta":
            products = products.order_by("-name")
        else:
            products = products.order_by("-id")

        
        l1 = []         # color cart
        for i in cart_item:
            l1.append(i.product_id.id)
        l2 = []        # color wishlist
        for i in wishlist_items:
            l2.append(i.product_id.id)  

        # Pagination
        paginator = Paginator(products, 3)
        page_number = request.GET.get("page", 1)

        try:
            page_number = int(page_number)
        except ValueError:
            page_number = 1

        products_page = paginator.get_page(page_number)
        show_page = paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1)

        con = {
            "uid": uid,
            "cid": cid,
            "pid": products_page,
            "price_show": price_show,
            "sorting": sorting,
            "show_page": show_page,
            "Additional_all": Additional.objects.all(),
            "Additional_fil": additional_filter,
            'l2':l2
        }

        return render(request, "shop.html", con)
    else:
        return render(request, "login.html")
      
def cart(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session["email"])
        cart_item = Add_to_cart.objects.filter(user_id=uid)  # Saare cart items user ke liye le rahe hain
        # (yah usi user ko product show hogi jo login hai)

        cart_item_count=Add_to_cart.objects.filter(user_id=uid).count()  # Count Cart Item
        Wishlist_item_count=Add_to_Wishlist.objects.filter(user_id=uid).count()
        
        if cart_item.count()==0:
            empty_cart="Your cart is empty." 
            con = {
                "uid":uid,
                "empty_cart":empty_cart,
               "cart_item_count":cart_item_count , 
               "Wishlist_item_count":Wishlist_item_count
            }
        pid = Product.objects.filter(id__in=[item.product_id.id for item in cart_item ])

        l1 = []
        subtotal = 0
        Shipping_charge = 200
        total_price = 0
        discount = 0
        if "discount" in request.session and cart_item.count()>=1:
            discount=request.session['discount']
        if "discount" in request.session and cart_item.count()==0:
            del request.session['discount']   
        if cart_item.count() >=1:
            Shipping_charge=200
        else:
            discount=0
        for i in cart_item:
            a = i.quantity * i.price
            l1.append(a)
            subtotal = sum(l1)
            total_price = subtotal + Shipping_charge - discount    

              
        con = {
            "subtotal":subtotal,
            "Shipping_charge":Shipping_charge,
            "total_price":total_price,
            "uid": uid,
            "pid":pid,
            "cart_item": cart_item,
            'discount':discount,
            "Wishlist_item_count":Wishlist_item_count,
             "cart_item_count":cart_item_count ,



        }
        return render(request, "cart.html", con)
    else:
        return render(request, "login.html")
from django.shortcuts import redirect
def add_to_cart(request, id):
    if "email" in request.session:
        uid = User.objects.get(email=request.session["email"])
        pid = Product.objects.get(id=id)
        cart_item = Add_to_cart.objects.filter(user_id=uid, product_id=pid).first()
        if cart_item:
            cart_item.quantity += 1
            cart_item.total_price = cart_item.price * cart_item.quantity
            cart_item.save()
        else:
            Add_to_cart.objects.create(
                user_id=uid,
                product_id=pid,
                name=pid.name,
                image=pid.image,
                quantity=1,
                price=pid.price,
                total_price=pid.price
            )
        # Redirect to the cart page after adding or updating the item(yaha pe render nahi kiya ja sakata hai)
        return redirect('cart')
    else:
        return redirect('login')

def increment(request, id):
    cart_item = Add_to_cart.objects.get(id=id)
    cart_item.quantity += 1
    cart_item.total_price = cart_item.price * cart_item.quantity
    cart_item.save()
    return redirect('cart')          

def decrement(request,id):
    add_items = Add_to_cart.objects.get(id = id)
    if add_items.quantity  > 1:
        add_items.quantity -=1
        add_items.total_price = add_items.price*add_items.quantity
        add_items.save()
    else:  
        add_items.delete()    
    return redirect("cart")

def add_to_cart_remove(request,id):
    add_items = Add_to_cart.objects.get(id=id)
    if add_items:
         add_items.delete()
    return redirect("cart")    


def Wish_list(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session["email"])
        wishlist_items = Add_to_Wishlist.objects.filter(user_id = uid)

        con={
            "wishlist_items":wishlist_items
        }
        return render(request,"Wish_list.html",con)
    else:
        return render(request,"login.html")

def add_to_Wishlist(request,id):
    if "email" in request.session:
        uid = User.objects.get(email = request.session["email"])
        pid = Product.objects.get(id=id)
        wishlist_items = Add_to_Wishlist.objects.filter(user_id=uid, product_id=pid).first()

        if wishlist_items:
           wishlist_items.delete()
           messages.error(request,"Your item removed from Wishlist")

        else:
            Add_to_Wishlist.objects.create(
                user_id = uid,
                product_id = pid,
                name = pid.name,
                image = pid.image,
                price = pid.price
                )
            messages.error(request,"Your item Saved in Wishlist")
        return redirect("shop")
    else:
        return render(request,"login.html")

def remove_Wishlist(request,id):
    wishlist_items = Add_to_Wishlist.objects.get(id=id)
    if wishlist_items:
        wishlist_items.delete()
    return redirect("Wish_list")

def chackout(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session["email"])
        cart_item = Add_to_cart.objects.filter(user_id=uid)
        
        if request.method == "POST":
            First_Name = request.POST["First_Name"]
            Last_Name = request.POST["Last_Name"]
            Company_Name = request.POST["Company_Name"]
            Address = request.POST["Address"]
            City = request.POST["City"]
            Country = request.POST["Country"]
            Mobile = request.POST["Mobile"]
            Email_Address = request.POST["Email_Address"]

            Chackout.objects.create(
                First_Name=First_Name,
                Last_Name=Last_Name,
                Company_Name=Company_Name,
                Address=Address,
                City=City,
                Country=Country,
                Mobile=Mobile,
                Email_Address=Email_Address
            )
            
            cart_data = []
            subtotal = 0
            Shipping_charge = 200
            total_price = 0
            discount = 0
            
            for i in cart_item:
                item_subtotal = i.quantity * i.price
                cart_data.append({
                    "item": i,
                    "image": i.image, 
                    "name": i.name,   
                    "price": i.price,  
                    "quantity": i.quantity,  
                    "subtotal": item_subtotal
                })
            
            # Calculate overall subtotal and total price
            subtotal = sum(item['subtotal'] for item in cart_data)
            total_price = subtotal + Shipping_charge - discount
            
            con = {
                "uid": uid,
                "cart_data": cart_data,
                "subtotal": subtotal,
                "Shipping_charge": Shipping_charge,
                "total_price": total_price,
                "discount": discount
               
            }

            messages.success(request, "Your details have been submitted successfully.")
            return render(request, "chackout.html", con)
        else:
            con = {
                "cart_data":cart_item,
                "user_name": uid.name,  
                "user_email": uid.email
              }
            return render(request, "chackout.html", con)
      
    else:
        return render(request, 'login.html')


def contact(request):
    if "email" in request.session:
        if request.POST:
            name= request.POST["name"]
            email=request.POST["email"]
            message=request.POST["message"]
            Contact.objects.create(name=name,email=email,message=message)
            messages.success(request,"Your Message submit successfully.")
            return redirect("contact")
        else:
            return render(request,'contact.html')
    else:
        return render(request,'login.html')

def register(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        try:
            # Check if User Email and  email
            uid = User.objects.get(email=email)
            con={"msg":"User allready Exist......"}
            return render(request, 'register.html',con)
        
        except User.DoesNotExist:
            # Check if password and confirm_password match
            if password == confirm_password:
                uid=User(name=name, email=email, password=password)
                uid.save()
                return redirect("login")
            else:    
                con={"msg":"Password do not match."}
                return render(request,"register.html",con)
    else:
        return render(request, 'register.html')      
     
   
def login(request):
    if "email" in request.session:  # Check कर रहे हैं कि session में email stored है या नहीं
        uid = User.objects.get(email=request.session["email"])  # अगर है, तो user को identify कर रहे हैं
        return render(request, "index.html")  # और उसे 'index.html' page पर redirect कर रहे हैं
    
    if request.method == "POST":  # अगर user ने login form submit किया है
        email = request.POST['email']  # form से email field को access कर रहे हैं
        password = request.POST["password"]  # password field को भी access कर रहे हैं

        try:
            uid = User.objects.get(email=email)  # User model में email से user को search कर रहे हैं
            if uid.password == password:  # password match कर रहे हैं
                request.session['email'] = uid.email  # अगर match हो गया, तो session में email store कर रहे हैं
                
                # Debugging: Print session data
                print("Session Data:", request.session.items())  # Session content को console में print कर रहे हैं
                
                return render(request, "index.html")  # user को index page पर redirect कर रहे हैं
            else:
                messages.error(request, "Invalid Password")  # अगर password गलत है, तो error message दिखा रहे हैं
                return render(request, 'login.html')  # और login page पर redirect कर रहे हैं

        except User.DoesNotExist:  # अगर user exist नहीं करता है, तो ये exception handle कर रहे हैं
            messages.error(request, "User Does Not Exist.")  # error message दिखा रहे हैं
            return render(request, "login.html")  # और login page पर redirect कर रहे हैं
    else:
        return render(request, 'login.html')  # अगर GET request है, तो login page को render कर रहे हैं


def log_out(request):
  if "email" in request.session:   
        del request.session["email"]
        return render(request,"login.html") 
  else:
        return render(request,"login.html")


import random
from django.core.mail import send_mail
def forgot(request):
    if request.POST:
        email=request.POST['email']
        otp=random.randint(1000,9999)
        try:
            uid = User.objects.get(email=email)
            uid.otp=otp
            uid.save()
            send_mail("django",f"your otp is - {otp}",'pareshbharda06@gmail.com',[email])
            contaxt={
                "email":email
            }
            return render(request,"reset_password.html",contaxt)
        except:
            messages.error(request,"User Not Exsist.....")      
            return render(request,"forgot.html") 
    else:
        return render(request,"forgot.html") 
    

def reset_password(request):
    if request.method == "POST":
        email= request.POST["email"]
        otp = request.POST["otp"]
        password = request.POST["password"]
        confirm_password = request.POST['confirm_password']

        try:
            uid = User.objects.get(email=email)
            if str(uid.otp) != str(otp):   #yah model mai to intiger le raha hai but as user ki orse yah str le raha hai.
                messages.error(request,"Invalaid OTP.....")
                return render(request,"reset_password.html")
            
            if password != confirm_password:
                messages.error(request,"Password dose Not match")
                return render(request,"reset_password.html")
            
            uid.password = confirm_password
            uid.save()
            messages.success(request,"Password reset successful.")
            return redirect('index')
         
        except User.DoesNotExist:
            messages.error(request,"User Dose Note Exist") 
            return render(request,"reset_password.html")

    return render(request,"reset_password.html")
                


    
def shop_detail(request,id):
    if "email" in request.session:
        uid = User.objects.get(email=request.session["email"])
        cat_id = Categories.objects.all()
        pid = Product.objects.get(id = id)
        con = {"uid":uid,
               "cat_id":cat_id,
               "pid":pid,
               }
        return render(request,"shop_detail.html",con)
    else:
        return render(request,"login.html")
    
def fack_detail(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session["email"])
        pid = Product.objects.all()
        add_items = Add_to_cart.objects.filter(user_id = uid)
       
        
        con = {"uid":uid,"pid":pid,"add_items":add_items
              
               }
        return render(request,"shop_detail.html",con)
    else:
        return render(request,"login.html")
    

    
def Price_filter(request):
    if request.POST:
        max1=request.POST['max1']
        print(max1)
        cid = Categories.objects.all()
        price_show = Price.objects.all()
        pid=Product.objects.filter(price__lte=max1)
        print("product",pid)
        con={"pid":pid,"max1":max1,"cid":cid,"price_show":price_show}

        return render(request,"shop.html",con)
    else:
        return render(request,"shop.html")
    
def Search_filter(request):
   
    search = request.GET.get("search")
    print(search)
    if search:
       pid=Product.objects.filter(name__contains=search)
    else:
        pid = Product.objects.all()   
       
    con={
            "pid":pid,
            "search":search
        }   
    return render(request,"shop.html",con)

def testimonial(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session["email"])
        all_product = Product.objects.all()
        filter_data = request.GET.get("filter_data")
        if filter_data:
            all_product = Product.objects.filter(price_id = filter_data)
        else:
            all_product = Product.objects.all()    

        con = {"uid":uid,
               "all_product" : all_product
               }
        
        return render(request,"testimonial.html",con)
    else:
        return render(request,"login.html")

def Related_products(request):
     if "email" in request.session:
        uid = User.objects.get(email=request.session["email"])
        pid_all = Product.objects.all()
        con={
            "pid":pid_all,
            "uid":uid
        }
        return render(request,"shop_detail.html",con)
     
     else:
         return render(request,"login.html")
       
#===============
from django.utils import timezone
def apply_coupon(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        aid = Add_to_cart.objects.filter(user_id=uid)
        l1 = []
        subtotal = 0
        Shipping_charge = 50
        for i in aid:
            l1.append(i.total_price)
        print(l1)
        subtotal = sum(l1)
        print("subtotal:- ", subtotal)
        total_price = subtotal + Shipping_charge
        print("total price : ", total_price)
        discount = 0
        if request.POST:
            coupon = request.POST['code']
            print("code:- ", coupon)
            caid = Coupon.objects.filter(code=coupon,one_time_use=True).exists()
            print("coupon:-", caid)
            if caid:
                cid = Coupon.objects.get(code=coupon)
                now_time = timezone.now()
                cid.one_time_use=False    #use coupon only one time then after false
                cid.save()
                if cid.expiry_date > now_time:
                    total_price -= cid.discount     
                    discount = cid.discount
                    request.session['discount'] = discount
                    con = {
                        "Shipping_charge": Shipping_charge, "subtotal": subtotal, "uid": uid,
                        "aid": aid, "discount": discount, "total_price": total_price}
                    messages.info(request, "Code applied successfully")
                    return redirect("cart")
                else:
                    cid.delete()
                    con = {
                        "Shipping_charge": Shipping_charge, "subtotal": subtotal, "uid": uid, "aid": aid,
                        "total_price": total_price, "discount": 0}
                    messages.info(request, "Coupon has expired and has been deleted")
                    return render(request, "cart.html", con)
            else:
                con = {
                    "Shipping_charge": Shipping_charge, "subtotal": subtotal, "uid": uid, "aid": aid,
                    "total_price": total_price, "discount": 0}
                messages.info(request, "No discount on this code")
                return redirect("cart")
        else:
            return render(request, "cart.html")
    else:   
        return render(request,"login.html")
#===============











        
       

        
        



    



