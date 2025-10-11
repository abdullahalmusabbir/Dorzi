from datetime import datetime, timedelta
from django.utils import timezone
from decimal import Decimal
from customer.models import *
from pre_designed.models import *
from custom_order.models import *
from reviews.models import *
from tailor.models import *
from dress_order.models import *
from embroidery.models import *
from fabrics.models import *
from favorite_dress.models import *
from favorite_tailor.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from functools import wraps
from django.contrib import messages  
from django.db.models import Q, Avg, Count, Sum, F, ExpressionWrapper, DecimalField
from django.core.exceptions import FieldError
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.http import require_POST

@login_required
def create_custom_orders(request, tailor_id):
    if request.method == 'POST':
        try:
            # Get the customer and tailor
            customer = Customer.objects.get(user=request.user)
            tailor = Tailor.objects.get(id=tailor_id)
            
            # Get form data
            full_name = request.POST.get('full_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            garment_type = request.POST.get('garment_type')
            
            # Handle multiple occasions (checkboxes)
            occasion_list = request.POST.getlist('occasion')
            occasion = ', '.join(occasion_list) if occasion_list else ''
            
            # Measurements - match the field names from your HTML form
            chest = request.POST.get('chest')
            waist = request.POST.get('waist')
            hips = request.POST.get('hips')  # Changed from 'hip' to 'hips'
            sleeve_length = request.POST.get('sleeve_length')
            garment_length = request.POST.get('length')  # This matches your HTML
            shoulder_width = request.POST.get('shoulder_width')
            neck_circumference = request.POST.get('neck')
            inseam_length = request.POST.get('inseam')

            
            # Design preferences
            fabric_preference = request.POST.get('fabric_preference')
            color_preference = request.POST.get('color_preference')
            design_inspiration = request.POST.get('design_inspiration')
            description = request.POST.get('description')
            special_request = request.POST.get('special_request', '')  # Changed from 'special_requests'
            
            # Handle embroidery selection and calculate total price
            embroidery_total_price = Decimal(request.POST.get('embroidery_total_price', 0))
            selected_embroidery_ids = request.POST.get('selected_embroidery_ids', '')
            
            # Calculate total price (tailor base price + embroidery total)
            base_price = tailor.price
            total_price = base_price + embroidery_total_price
            
            # Calculate delivery date (21 working days from now)
            delivery_date = calculate_working_days(datetime.now().date(), 21)
            
            # Create the custom order
            custom_order = TOrders.objects.create(
                customer=customer,
                tailor=tailor,
                
                # Contact information
                address=address,
                contact_number=phone,
                gender=gender,
                
                # Order details
                occasion=occasion,
                garment_type=garment_type,
                
                # Design preferences
                fabrics=fabric_preference,
                color=color_preference,
                inspiration=design_inspiration,
                detailed_description=description,
                special_requests=special_request,
                delivery_date=delivery_date,
                price=total_price,  # Now includes embroidery prices
                
                # Measurements - match the TOrders model fields
                chest=chest,
                waist=waist,
                hip=hips,  # Using the 'hips' value for 'hip' field
                shoulder=shoulder_width,
                sleeve=sleeve_length,
                neck=neck_circumference,
                length=garment_length,
                inseam=inseam_length,
                
                # Set initial status
                status='pending',
            )
            
            # Handle embroidery selection if any
            if selected_embroidery_ids:
                embroidery_id_list = [int(id) for id in selected_embroidery_ids.split(',') if id.strip()]
                selected_embroideries = Embroidery.objects.filter(id__in=embroidery_id_list, tailor=tailor)
                
                # Store embroidery info if you have the field in your model
                # If you have a ManyToMany field, use:
                # custom_order.embroidery_designs.add(*selected_embroideries)
                
                # Or store as JSON if you have a JSON field
                if hasattr(custom_order, 'selected_embroidery_info'):
                    custom_order.selected_embroidery_info = json.dumps([
                        {
                            'id': emb.id,
                            'title': emb.title,
                            'price': str(emb.price)
                        } for emb in selected_embroideries
                    ])
                    custom_order.save()
            
            messages.success(request, f"Custom order placed successfully! Your order ID is TORD-{custom_order.id:03d}. Total price: ৳{total_price}")
            return redirect('customer')
            
        except Customer.DoesNotExist:
            messages.error(request, "Customer profile not found.")
            return redirect('findTailor')
        except Tailor.DoesNotExist:
            messages.error(request, "Selected tailor does not exist.")
            return redirect('findTailor')
        except Exception as e:
            messages.error(request, f"Error creating custom order: {str(e)}")
            return redirect('findTailor')
    
    # If GET request, redirect back to findTailor page
    return redirect('findTailor')
  
@login_required
def create_order(request):
    if request.method == 'POST':
        try:
            # Get form data
            product_id = request.POST.get('product_id')
            tailor_id = request.POST.get('tailor_id')
            quantity = int(request.POST.get('quantity', 1))
            price = Decimal(request.POST.get('price', 0))
            size = request.POST.get('size', 'S')
            full_name = request.POST.get('full_name')
            phone = request.POST.get('phone')
            address = request.POST.get('address')
            special_instructions = request.POST.get('special_instructions', '')
            
            # Validate required fields
            if not all([product_id, tailor_id, full_name, phone, address]):
                messages.error(request, "Please fill in all required fields.")
                return redirect('pre_designed')
            
            # Validate quantity and price
            if quantity <= 0:
                messages.error(request, "Quantity must be at least 1.")
                return redirect('pre_designed')
            
            if price <= 0:
                messages.error(request, "Invalid price.")
                return redirect('pre_designed')
            
            # Get objects with error handling
            try:
                product = PreDesigned.objects.get(id=product_id)
                tailor = Tailor.objects.get(id=tailor_id)
            except PreDesigned.DoesNotExist:
                messages.error(request, "Selected product does not exist.")
                return redirect('pre_designed')
            except Tailor.DoesNotExist:
                messages.error(request, "Selected tailor does not exist.")
                return redirect('pre_designed')
            
            # Create the order
            order = Order.objects.create(
                customer=request.user,
                tailor=tailor,
                product=product,
                quantity=quantity,
                price=price,
                address=address,
                number=phone,
                size=size,
                category=product.category,
                special_instructions=special_instructions,
                delivery_date=timezone.now() + timedelta(days=10)  # 10 days from now
            )
            
            messages.success(request, f"Order placed successfully! Your order ID is #{order.id}")
            return redirect('customer')
            
        except ValueError as e:
            messages.error(request, f"Invalid input: {str(e)}")
            return redirect('pre_designed')
        except Exception as e:
            messages.error(request, f"Error creating order: {str(e)}")
            return redirect('pre_designed')
    
    # If not POST request, redirect to pre_designed page
    return redirect('pre_designed')

def tailor_signup(request):
    if request.method == 'POST':
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        business_name = request.POST.get('business_name')
        specialization = request.POST.get('specialization')
        experience = request.POST.get('experience')
        business_location = request.POST.get('business_location')
        nid_number = request.POST.get('nid_number')
        profile_picture = request.FILES.get('profile_picture')
        tailor_about = request.POST.get('tailor_about')
        business_description = request.POST.get('business_description')
        address = request.POST.get('address')
        
        # Validate passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('user_signup')
            
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('user_signup')
            
        try:
            # Create User
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name.split()[0] if full_name else '',
                last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
            )
            
            # Create Tailor
            tailor = Tailor.objects.create(
                user=user,
                business_name=business_name,
                business_location=business_location,
                phone=phone,
                NID=nid_number,
                profile_picture=profile_picture,
                services_offered=specialization,
                expertise=experience,
                category=specialization,
                average_rating=0.0,
                is_available=True,
                tailor_about=tailor_about,
                business_description=business_description,
                address=address
            )
            
            # Log the user in
            auth_login(request, user)
            messages.success(request, "Tailor account created successfully!")
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('user_signup')
    
    return render(request, 'signup.html')

def tailor_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # This should be the email
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user has a tailor profile
            if hasattr(user, 'tailor'):
                auth_login(request, user)
                
                # Set session expiry based on remember me
                if remember_me:
                    # Session will expire after 2 weeks (remember me checked)
                    request.session.set_expiry(1209600)  # 2 weeks in seconds
                else:
                    # Session will expire when browser is closed (remember me not checked)
                    request.session.set_expiry(0)
                
                messages.success(request, "You have successfully logged in as a tailor!")
                return redirect('tailor_dashboard')
            else:
                messages.error(request, "This account is not registered as a tailor!")
                return redirect('user_login')
        else:
            messages.error(request, "Invalid email or password!")
            return redirect('user_login')
    
    return render(request, 'user_login.html')

@login_required
def addDress(request):
    if request.method == 'POST':
        try:
            # Debugging: Check if request is reaching here
            print("AddDress POST request received")
            print("POST data:", request.POST)
            print("FILES:", request.FILES)
            
            # Get the current tailor
            tailor = Tailor.objects.get(user=request.user)
            print("Tailor found:", tailor)
            
            # Create the PreDesigned object
            dress = PreDesigned.objects.create(
                tailor=tailor,
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                availability=int(request.POST.get('availability', 0)),
                price=Decimal(request.POST.get('price', 0.0)),
                category=request.POST.get('category', ''),
                fabric_type=request.POST.get('fabric_type', ''),
                thread_type=request.POST.get('thread_type', ''),
                color=request.POST.get('color', ''),
                gender=request.POST.get('gender', '')
            )
            
            # Handle estimated time
            estimated_time = request.POST.get('estimated_time')
            if estimated_time and estimated_time.isdigit():
                dress.estimated_time = timedelta(hours=int(estimated_time))
            
            dress.save()
            print("Dress object created:", dress.id)
            
            # Handle multiple image uploads
            images = request.FILES.getlist('images')
            print("Images received:", len(images))
            
            for image in images:
                Image.objects.create(predesigned=dress, image=image)
                print("Image saved:", image.name)
            
            messages.success(request, "Dress added successfully!")
            return redirect('tailor_dashboard')
            
        except Exception as e:
            print("Error in addDress:", str(e))
            messages.error(request, f"Error adding dress: {str(e)}")
            return redirect('tailor_dashboard')  # Redirect back to dashboard
    
    # If GET request, this shouldn't happen from modal
    messages.error(request, "Invalid request method")
    return redirect('tailor_dashboard')

@login_required
def get_dress_details(request, product_id):
    try:
        # Get the product
        product = PreDesigned.objects.get(id=product_id)
        
        # Check if the current user owns this product
        if product.tailor.user != request.user:
            return JsonResponse({'success': False, 'error': 'You do not have permission to view this product.'})
        
        # Get all images for this product
        images = [request.build_absolute_uri(image.image.url) for image in product.images.all()]
        
        # Prepare response data
        data = {
            'success': True,
            'product': {
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'price': str(product.price),
                'category': product.category,
                'availability': product.availability,
                'fabric_type': product.fabric_type,
                'thread_type': product.thread_type,
                'color': product.color,
                'estimated_time': str(product.estimated_time) if product.estimated_time else None,
                'created_at': product.created_at.isoformat(),
                'updated_at': product.updated_at.isoformat(),
            },
            'images': images
        }
        
        return JsonResponse(data)
        
    except PreDesigned.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def createreviews(request):
    return render(request, 'createreviews.html')

def deletereviews(request):
    return render(request, 'deletereviews.html')

def updatereviews(request):
    return render(request, 'updatereviews.html')

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('user_signup')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('user_signup')
            
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=full_name.split()[0] if full_name else '',
                last_name=' '.join(full_name.split()[1:]) if len(full_name.split()) > 1 else ''
            )
            customer = Customer.objects.create(
                user=user,
                phone=phone,
                address=address
            )
            
            auth_login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('user_login')  
            
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return redirect('user_signup')
    
    return render(request, 'signup.html')

def logout(request):
    auth_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # This should be the email
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Optional remember me functionality

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login the user
            auth_login(request, user)
            
            # Set session expiry based on remember me
            if remember_me:
                # Session will expire after 2 weeks (remember me checked)
                request.session.set_expiry(1209600)  # 2 weeks in seconds
            else:
                # Session will expire when browser is closed (remember me not checked)
                request.session.set_expiry(0)
            
            messages.success(request, "You have successfully logged in!")
            
            # Redirect to appropriate dashboard based on user type
            if hasattr(user, 'tailor'):
                return redirect('tailor_dashboard')
            else:
                return redirect('customer')
        else:
            messages.error(request, "Invalid email or password!")
            return redirect('user_login')
    
    # If GET request, show login form
    return render(request, 'user_login.html')

def customer(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    products =  PreDesigned.objects.all()
    torder = TOrders.objects.filter(customer=customer).order_by('-order_date')
    dressorder = Order.objects.filter(customer=user).order_by('-order_date')
    favorite_dresses = FavoriteDress.objects.filter(user=customer)
    favorite_tailors = FavoriteTailor.objects.filter(user=customer)

    all_orders = []
    for order in torder:
        if order.deliver is not None:
            status = "Completed"
        else:
            status = "Pending"
        all_orders.append({
            'id': order.id,
            'order_id': f"TORD-{order.id:03d}",
            'garment': order.detailed_description or "Custom Garment",
            'category': order.category or "Custom",
            'tailor': order.tailor,
            'delivery_date': order.delivery_date,
            'status': order.status,
            'order_type': "Custom Order",
            'amount': order.get_total_price(),
            'progress': None,  # This is the important field for custom orders
            'timeline': order.status if hasattr(order, 'timeline') else {},
            'order_date': order.order_date if hasattr(order, 'order_date') else None,
            # Custom order specific fields
            'fabric': order.fabrics if hasattr(order, 'fabrics') else '',
            'color': getattr(order, 'color', ''),
            'chest': order.chest,
            'waist': order.waist,
            'hip': order.hip,
            'shoulder': order.shoulder,
            'sleeve': order.sleeve,
            'length': order.length,
            'inseam': order.inseam,
            'neck': order.neck,
            'special_notes': order.special_requests if hasattr(order, 'special_requests') else '',
            # Custom orders 
            'measurements_confirmed': getattr(order, 'measurements_confirmed', None),
            'fabric_selected': getattr(order, 'fabric_selected', None),
            'cutting_started': getattr(order, 'cutting_started', None),
            'stitching_started': getattr(order, 'stitching_started', None),
            'deliver': getattr(order, 'deliver', None),
        })
    
    # Process Pre-designed orders
    for order in dressorder:
        if order.deliver is not None:
            status = "Completed"
        else:
            status = "Pending"
        all_orders.append({
            'id': order.id,
            'order_id': f"DORD-{order.id:03d}",
            'garment': order.product.title if order.product else "Pre-designed Garment",
            'category': order.category or "Pre-designed",
            'tailor': order.tailor,
            'delivery_date': order.delivery_date,
            'status': status,
            'order_type': "Pre-designed",
            'amount': order.get_total_price(),
            'progress': None,
            'timeline': order.status if hasattr(order, 'timeline') else {},
            'order_date': order.order_date if hasattr(order, 'order_date') else None,
            'size': order.size if hasattr(order, 'size') else None,
            # Pre-designed order specific fields
            'fabric': order.product.fabric_type if order.product else '',
            'color': order.product.color if order.product else '',
            'quantity': order.quantity,
            'special_instructions': order.special_instructions if hasattr(order, 'special_instructions') else '',
            # Pre-designed orders 
            'order_confirmed': getattr(order, 'order_confirmed', None),
            'production': getattr(order, 'production', None),
            'quality_check': getattr(order, 'quality_check', None),
            'deliver': getattr(order, 'deliver', None),
        })
    
    # Sort by delivery_date safely
    all_orders.sort(key=lambda x: x['delivery_date'] if x['delivery_date'] else datetime.min, reverse=True)
    
    # Stats
    total_orders = len(all_orders)
    completed_orders = len([order for order in all_orders if order['status'].lower() == 'delivered'])
    pending_orders = len(all_orders) - completed_orders
    favorite_tailors_count = favorite_tailors.count()
    
    return render(request, 'customer.html', {
        'customer': customer,
        'torder': torder,
        'dressorder': dressorder,
        'favorite_dresses': favorite_dresses,
        'favorite_tailors': favorite_tailors,
        'all_orders': all_orders,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'pending_orders': pending_orders,
        'favorite_tailors_count': favorite_tailors_count,
        'products': products
    })

@login_required
def addEmbroidery(request):
    if request.method == 'POST':
        try:
            # Get the current tailor
            tailor = Tailor.objects.get(user=request.user)
            
            # Create the Embroidery object
            embroidery = Embroidery.objects.create(
                tailor=tailor,
                title=request.POST.get('title'),
                description=request.POST.get('description', ''),
                price=request.POST.get('price', 0.0),
                fabric_type=request.POST.get('fabric_type', ''),
                thread_type=request.POST.get('thread_type', ''),
                color=request.POST.get('color', ''),
                complexity_level=request.POST.get('complexity_level', 'simple'),
            )
            
            # Handle estimated time (convert hours to timedelta)
            estimated_time_hours = request.POST.get('estimated_time')
            if estimated_time_hours:
                embroidery.estimated_time = timedelta(hours=int(estimated_time_hours))
            
            # Handle image upload
            design_image = request.FILES.get('design_image')
            if design_image:
                embroidery.design_image = design_image
            
            embroidery.save()
            
            messages.success(request, "Embroidery design added successfully!")
            return redirect('tailor_dashboard')
            
        except Exception as e:
            messages.error(request, f"Error adding embroidery design: {str(e)}")
            return redirect('addEmbroidery')
    
    # If GET request, show the form
    return render(request, 'addEmbroidery.html')    

@login_required
def get_embroidery_details(request, embroidery_id):
    try:
        # Get the embroidery design
        embroidery = Embroidery.objects.get(id=embroidery_id)
        
        # Check if the current user owns this embroidery design
        if embroidery.tailor.user != request.user:
            return JsonResponse({'success': False, 'error': 'You do not have permission to view this embroidery design.'})
        
        # Prepare response data
        data = {
            'success': True,
            'embroidery': {
                'id': embroidery.id,
                'title': embroidery.title,
                'description': embroidery.description,
                'price': str(embroidery.price),
                'fabric_type': embroidery.fabric_type,
                'thread_type': embroidery.thread_type,
                'color': embroidery.color,
                'complexity_level': embroidery.complexity_level,
                'estimated_time': str(embroidery.estimated_time) if embroidery.estimated_time else None,
                'design_image': request.build_absolute_uri(embroidery.design_image.url) if embroidery.design_image else None,
                'created_at': embroidery.created_at.isoformat(),
                'updated_at': embroidery.updated_at.isoformat(),
            }
        }
        
        return JsonResponse(data)
        
    except Embroidery.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Embroidery design not found.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
