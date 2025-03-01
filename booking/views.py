from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage , EmailMultiAlternatives
from email.mime.image import MIMEImage
from store.models import Event
from orders.models import Order, Payment, OrderEvent, UserEvent
from orders.forms import OrderForm
from accounts.models import UserProfile
from carts.models import Cart, CartItem
import os, json
import datetime
from .barcode_printer import OrderBarCodePrinter

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_booking(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        selected_seats=[]
        selected_seats_str = request.POST['selected_seats']
        if len(selected_seats_str):
            selected_seats = selected_seats_str.strip().split(',')
            # update json file 
            json_file_path= os.path.abspath(event.get_json_path())
            with open(json_file_path,'r') as jfp:
                hall_status = json.load(jfp)
            try:
                for k, seat in hall_status.items():
                    if seat['status']== 3:
                        seat['status'] = 0
                for seat in selected_seats:
                    hall_status[seat]['status'] = 4 
                with open(json_file_path,'w') as jfp:
                    json.dump(hall_status,jfp, indent=2)
            except:
                print('Something wrong!')
        # return HttpResponse("The method is POST and we got {} as selected seats".format(all_data))
    
    if len(selected_seats):
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()
        for seat in selected_seats:
            try:
                cart_item = CartItem.objects.get(event=event, cart=cart, seat=seat)
            except CartItem.DoesNotExist:
                cart_item = CartItem.objects.create(
                    event = event,
                    cart = cart,
                    seat = seat,
                    ingresso = 2,
                    price = event.price_full,
                    
                    
                )
                if request.user.is_authenticated:
                    cart_item.user=request.user
                    
                cart_item.save()
    else:
        return HttpResponse("<H1>Nessun posto selezionato message error</H1><br><a href='/'>Torna al cartellone</a>")
    
    request.session['active_cart_id'] = cart.cart_id

    return redirect('bookings')

def remove_booking(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    seat = item.seat
    event = item.event
    item.delete()
    json_file_path= os.path.abspath(event.get_json_path())
    with open(json_file_path,'r') as jfp:
        hall_status = json.load(jfp)
    try:
        if hall_status[seat]['status'] == 3 or hall_status[seat]['status'] == 4:
            hall_status[seat]['status'] = 0 
            with open(json_file_path,'w') as jfp:
                json.dump(hall_status,jfp, indent=2)
    except:
        print('Something wrong!')
    return redirect('bookings')


def plus_ing_booking(request, item_id = None):
    item = CartItem.objects.get(id=item_id)
    ingresso_old = item.ingresso
    if ingresso_old < 2:
        ingresso_new = ingresso_old + 1
    else:
        ingresso_new = 2
    item.ingresso = ingresso_new
    if ingresso_new == 0:
        item.price = 0.0
    elif ingresso_new == 1:
        item.price = item.event.price_reduced
    elif ingresso_new == 2:
        item.price = item.event.price_full

    item.save()

    # return HttpResponse('<H1>CartItem number {} move ingresso from {} to {}</H1>'.format(item_id, ingresso_old, ingresso_new))
    return redirect('bookings')


def minus_ing_booking(request, item_id = None):
    item = CartItem.objects.get(id=item_id)
    ingresso_old = item.ingresso
    if ingresso_old > 0:
        ingresso_new = ingresso_old - 1
    else:
        ingresso_new = 0
    item.ingresso = ingresso_new
    if ingresso_new == 0:
        item.price = 0.0
    elif ingresso_new == 1:
        item.price = item.event.price_reduced
    elif ingresso_new == 2:
        item.price = item.event.price_full
    item.save()

    # return HttpResponse('<H1>CartItem number {} move ingresso from {} to {}</H1>'.format(item_id, ingresso_old, ingresso_new))
    return redirect('bookings')

def bookings(request, total=0, cart_items=None):
    prices=[]
    vat_rate = 0.0
    try: 
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            if cart_items:
                cart = cart_items[0].cart
            else:
                cart = None

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        # active_cart_id = request.session['active_cart_id']
        # cart = Cart.objects.get(cart_id=active_cart_id)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for item in cart_items:
            vat_rate = item.event.vat_rate
            prices = [0.00, item.event.price_reduced, item.event.price_full]
            total += (prices[item.ingresso])
        taxable = int(total / (1 + vat_rate / 100) *100)/100
        tax = int((total - taxable) *100)/100

        context = {
            'cart': cart,
            'cart_items': cart_items,
            'total': total,
            'taxable': taxable,
            'tax': tax,
            'vat_rate': vat_rate,
            'prices': prices,
        }
    except ObjectDoesNotExist:
        context = {}

    return render(request, 'store/bookings.html', context)

@login_required(login_url='login')
def checkout_booking(request, total=0, cart_items=None):
    taxable = 0.0
    tax = 0.0
    vat_rate = 10 # % IVA
    try: 
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            if cart_items:
                cart = cart_items[0].cart
            else:
                cart = None

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_items:
            vat_rate = item.event.vat_rate
            total += item.price
            taxable += int(item.price / (1 + vat_rate / 100) *100)/100
        
        tax = int((total - taxable) *100)/100

        current_user = request.user
        try:
            former_order = Order.objects.filter(user=current_user).order_by('-created_at').first()
            user_data = {
            'user': current_user,
            'first_name': former_order.first_name,
            'last_name': former_order.last_name,
            'phone': former_order.phone,
            'email': former_order.email,
            'address_line_1': former_order.address_line_1,
            'address_line_2': former_order.address_line_2,
            'post_code': former_order.post_code,
            'city': former_order.city,
            'province': former_order.province,
            'order_note': former_order.order_note,
            }

        except:
            userprofile = UserProfile.objects.get(user=current_user)

            user_data = {
            'user': current_user,
            'first_name': userprofile.user.first_name,
            'last_name': userprofile.user.last_name,
            'phone': userprofile.user.phone_number,
            'email': userprofile.user.email,
            'address_line_1': userprofile.address_line1,
            'address_line_2': userprofile.address_line2,
            'post_code': userprofile.post_code,
            'city': userprofile.city,
            'province': userprofile.province,
            'order_note': '',

            }



        context = {
            'user_data': user_data,
            'cart': cart,
            'cart_items': cart_items,
            'total': total,
            'taxable': taxable,
            'tax': tax,
            'vat_rate': vat_rate,
        }
    except ObjectDoesNotExist:
        context = {}
    return render(request, 'booking/checkout.html', context)

def record_booking(request):
    current_user = request.user

    # If the cart count is less or equal to zero
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')
    
    grand_total = 0
    grouped_cart_items = {}
    for item in cart_items:
        vat_rate = item.event.vat_rate
        price = round_euro(item.price)
        taxable = round_euro(price / (1 + vat_rate / 100))
        tax = round_euro(price - taxable) 
        if item.event.event_slug in grouped_cart_items:
            grouped_cart_items[item.event.event_slug]['count'] += 1
            grouped_cart_items[item.event.event_slug]['price_tot'] += price
            grouped_cart_items[item.event.event_slug]['taxable_tot'] += taxable
            grouped_cart_items[item.event.event_slug]['tax_tot'] += tax
            grouped_cart_items[item.event.event_slug]['seat'] += ', '+item.seat

        else:
            grouped_cart_items[item.event.event_slug]= {}
            grouped_cart_items[item.event.event_slug]['count'] = 1
            grouped_cart_items[item.event.event_slug]['price_tot'] = price
            grouped_cart_items[item.event.event_slug]['taxable_tot'] = taxable
            grouped_cart_items[item.event.event_slug]['tax_tot'] = tax
            grouped_cart_items[item.event.event_slug]['seat'] = item.seat
            grouped_cart_items[item.event.event_slug]['event'] = item.event

    taxable = 0.0
    tax = 0.0

    for k, item in grouped_cart_items.items():
        grand_total += item['price_tot']
        taxable += item['taxable_tot']
        tax += item['tax_tot'] 

    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order Table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.post_code = form.cleaned_data['post_code']
            data.city = form.cleaned_data['city']
            data.province = form.cleaned_data['province']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save() 

            # Generate order number
            order_number = f"{data.id:06d}"
            data.order_number = order_number
            data.save()

            del data

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            del order_number
            # change for booking only - the payment_required is always FALSE
            payment_required: int = 0

            body = {
                    'orderID': order.order_number,
                    'transID': order.order_number,
                    'payment_method': 'none',
                    'status': 'BOOKED'
                    }


            context = {
                'payment_required': payment_required,
                'order': order,
                'cart_items': cart_items,
                'total': taxable,
                'grand_total': grand_total,
                'tax': tax,
                'cart_count': cart_count,
                'grouped_cart_items' : grouped_cart_items,
                'body': body,

            }

            # for booking only no payment page is shown, direct to record the void payments data
            response = booking_payments(request, context)
            return response
        else:
            return HttpResponse("<H1>Entered the POST clause</H1><br>Got the following form that is NOT VALID <br> {}".format(form))

    else:
        return redirect('bookings')
    
def booking_payments(request, newContext={}):
    current_user = request.user
    body = newContext['body']
    #print(body)
    order = Order.objects.get(user=current_user, is_ordered=False, order_number= body['orderID'])
    payment = Payment(
        user=current_user,
        payment_id=body['transID'],
        payment_method=body['payment_method'],
        amount_paid= 0.00,
        status=body['status'],
        # payer_id=body['payer']['payer_id'],
        payer_mail=current_user.email,
        payer_surname=current_user.last_name,
        payer_given_name=current_user.first_name,
        )
    payment.save()
    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move the cart items to the Order Product table and modifiy the Hall Status Json file of event

    cart_items = CartItem.objects.filter(user=request.user).order_by('event')


    # prepare a dictionary for email data
    email_data = {}


    for item in cart_items:
        seat= item.seat
        event = item.event

        #Manage the OrderEvent record 
        try:
            orderevent = OrderEvent.objects.get(user=current_user, event=event, order=order)
            items = orderevent.seats_price
            items += ',{}${}'.format(seat, item.ingresso)
            orderevent.seats_price = items
            # update email data
            booked_seats[seat] = item.price            
            email_data[orderevent.orderevent_number]['seats'] = booked_seats
            orderevent.save()
        except:
            items = '{}${}'.format(seat, item.ingresso)
            orderevent = OrderEvent(
            order = order,
            payment = payment,
            event = event,
            user = current_user,
            seats_price = items
            )
            orderevent.save()
            orderevent.orderevent_number = f'{orderevent.event.pk:05d}_{order.order_number}_{orderevent.pk:06d}'
            orderevent.save()


            barcode_printer = OrderBarCodePrinter(
                save_path = 'images',
                numero=orderevent.orderevent_number ,
                )
            barcode_image_path: os.path = barcode_printer.make_barcode()
            orderevent.barcode_path = barcode_image_path
            orderevent.save()
            booked_seats = {}
            booked_seats[seat] = item.price

            email_data[orderevent.orderevent_number] = {
            'show':orderevent.event.show.shw_title,
            'datetime': orderevent.event.date_time,
            'seats': booked_seats,
            'barcode': orderevent.barcode_path.split('/')[-1],
            'barcode_path': orderevent.barcode_path 
            }


        # Update the Json file of event 
        json_filename_fullpath = event.get_json_path()
        if os.path.exists(json_filename_fullpath):
            with open(json_filename_fullpath,'r') as fp:
                event_hall = json.load(fp)
            event_hall[seat]['status'] = 1  # set status to BOOKED 
            event_hall[seat]['order'] = orderevent.orderevent_number  # set order to orderevent_number 
            with open(json_filename_fullpath,'w') as fp:
                json.dump(event_hall,fp,indent=4, separators=(',', ': '))
        else:
            print('Problems with {} file doesnt exist!'.format(json_filename_fullpath))

        # Manage the UserEvent record (cross table connecting all orders of one user to one event
        # collecting all setas and prices of User for One event)
        try:
            userevent = UserEvent.objects.get(user=current_user, event=event)
            ordersevents = userevent.ordersevents
            if str(orderevent.pk) not in ordersevents:
                ordersevents += ',{}'.format(orderevent.pk)
                userevent.ordersevents = ordersevents
            userevent.save()
        except:
            userevent = UserEvent()
            userevent.ordersevents = str(orderevent.pk)
            userevent.event = event
            userevent.user = current_user
            userevent.save()





    # Clear the cart

    CartItem.objects.filter(user=current_user).delete()

    # Count the order events included in the single order
    orderevents_count = len(email_data)

    # Send order received email to customer 

    current_site = get_current_site(request)

    mail_subject = 'LTC BoxOffice. Grazie per la tua prenotazione!'
    email_context = {
        'count': orderevents_count,
        'user': request.user,
        'order': order,
        'userevent': userevent,
        'email_data' : email_data,
    }
    message = render_to_string('booking/multibooking_received_email.html', email_context).strip()
    if current_user.email == order.email:
        to_email = [current_user.email,]
    else:
        to_email = [current_user.email,order.email,]
    # send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email = EmailMultiAlternatives(
        mail_subject,
        message,
        to=to_email
    )
    send_email.content_subtype = 'html'
    send_email.mixed_subtype = 'related'
    # send_email.attach(message, "text/html")
    img_dir = 'static/images'
    image = 'logo.png'
    file_path = os.path.join(img_dir, image)
    with open(file_path,'rb') as fip:
        img = MIMEImage(fip.read(),_subtype='png')
        img.add_header('Content-ID', '<{name}>'.format(name=image))
        # img.add_header('Content-Disposition', 'inline', filename=image)
    send_email.attach(img)

    for orderevent_number, orderevent_data in email_data.items():
        file_path:os.path = orderevent_data['barcode_path']
    #this name must be same as in the htmltemplate being only a placeholder
        barcode:str = orderevent_data['barcode']

        with open(file_path,'rb') as fip:
            brc = MIMEImage(fip.read(),_subtype='png')
            brc.add_header('Content-ID', '<{name}>'.format(name=barcode))
            # img.add_header('Content-Disposition', 'inline', filename=image)
        send_email.attach(brc)

    send_email.send()

    # Send order number and transaction id back to sendData method via JsonResponse

    order.status = None

    newContext['data'] = {
        'order_number': order.order_number,
        'transID': payment.payment_id,
        'barcode': barcode_image_path,
        'email_data': email_data,
    }

    response = booking_complete(request, newContext)

    return response

def booking_complete(request, newContext={}):
    order_number = newContext['data']['order_number']
    transID = newContext['data']['transID']
    email_data = newContext['data']['email_data']
    for number, orderevent in email_data.items():
        newtarget:os.path = os.path.join(os.getcwd(),'ltcboxoffice/static/images',orderevent['barcode'])
        if newtarget != orderevent['barcode_path']:
            file_available: bool = False
            # cnt_idle_cycle = 0
            while not file_available:
                # cnt_idle_cycle +=1
                file_available: bool = os.path.isfile(orderevent['barcode_path']) and os.access(orderevent['barcode_path'], os.R_OK)

            # print(f'idle for {cnt_idle_cycle} cycles')
            os.rename(orderevent['barcode_path'],newtarget)
        orderevent_object = OrderEvent.objects.get(orderevent_number=number)
        orderevent_object.barcode_path = newtarget
        orderevent_object.save()

    del number, orderevent, newtarget
    

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        orderevents = OrderEvent.objects.filter(order_id=order.id)
        #set the order status to completed
        order.status = Order.STATUS[2][-1]
        order.save()
        payment = Payment.objects.get(payment_id=transID)
        context = {
            'order': order,
            'orderevents': orderevents,
            'payment': payment,
            'emaildata': email_data,
        }
        return render(request, 'booking/booking_complete.html', context)
    except (Order.DoesNotExist, Payment.DoesNotExist):
        return redirect('home')

def round_euro(the_float):
    return int(the_float * 100 + 0.5) / 100
