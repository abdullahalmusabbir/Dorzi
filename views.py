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
  
