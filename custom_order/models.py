from django.db import models
from django.contrib.auth.models import User  
from django.utils.timezone import now
from tailor.models import Tailor
from fabrics.models import Fabrics  

class CustomOrder(models.Model):
    GARMENT_TYPE_CHOICES = [
        # Punjabi
            ('short_punjabi', 'Short Punjabi'),
            ('long_punjabi', 'Long Punjabi'),
            ('designer_punjabi', 'Designer Punjabi'),
            ('embroidered_punjabi', 'Embroidered Punjabi'),
            ('kurta_punjabi', 'Kurta Punjabi'),
            ('traditional_punjabi', 'Traditional Punjabi'),

            # Shirt
            ('formal_shirt', 'Formal Shirt'),
            ('casual_shirt', 'Casual Shirt'),
            ('half_sleeve_shirt', 'Half Sleeve Shirt'),
            ('denim_shirt', 'Denim Shirt'),
            ('tshirt', 'T-Shirt'),
            ('sleeveless_shirt', 'Sleeveless Shirt'),
            ('printed_shirt', 'Printed Shirt'),

            # Pant
            ('kurta', 'Kurta'),
            ('formal_pant', 'Formal Pant'),
            ('jeans', 'Jeans'),
            ('cargo_pant', 'Cargo Pant'),
            ('chinos', 'Chinos'),
            ('trouser', 'Trouser'),
            ('shorts', 'Shorts'),
            ('leggings', 'Leggings'),

            # Women’s Dress
            ('salwar_kameez', 'Salwar Kameez'),
            ('lehenga', 'Lehenga'),
            ('blouse', 'Blouse'),
            ('saree_fall_pleat', 'Saree Fall & Pleat'),
            ('gown', 'Gown'),
            ('maxi_dress', 'Maxi Dress'),
            ('anarkali', 'Anarkali'),
            ('skirt', 'Skirt'),
            ('palazzo', 'Palazzo'),
            ('tops', 'Tops'),
            ('kameez', 'Kameez'),
            ('saree_blouse', 'Saree Blouse'),
            ('waistcoat', 'Waistcoat'),
            ('jacket', 'Jacket'),
            ('coat', 'Coat'),
            ('sherwani', 'Sherwani'),
            ('kids_dress', 'Kids Dress'),
        ('other', 'Other'),
    ]
    OCCASION_CHOICES = [
        ('wedding', 'Wedding'),
        ('festival', 'Festival'),
        ('office_formal', 'Office/Formal'),
        ('casual_daily_wear', 'Casual Daily Wear'),
        ('party_event', 'Party/Event'),
        ('religious_ceremony', 'Religious Ceremony'),
        ('business_meeting', 'Business Meeting'),
        ('date_night', 'Date Night'),
        ('travel', 'Travel'),
        ('other', 'Other'),
    ]

    CUSTOMER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
        ('N/A', 'N/A'),
    ]
    TAILOR_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'), 
    ]
    
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_orders')
    tailor = models.ForeignKey(Tailor, on_delete=models.CASCADE, related_name='custom_orders')
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    contact_number = models.CharField(max_length=11, blank=True, null=True)  
    customer_status = models.CharField(max_length=20, choices=CUSTOMER_STATUS_CHOICES, default='pending') 
    tailor_status = models.CharField(max_length=20, choices=TAILOR_STATUS_CHOICES, default='pending')  
    size = models.CharField(max_length=20)  
    description = models.TextField() 
    delivery_date = models.DateField(blank=True, null=True)  
    date = models.DateTimeField(auto_now_add=True, editable=False)
    garment_type = models.CharField(max_length=30, choices=GARMENT_TYPE_CHOICES, default='other')
    occasion = models.CharField(max_length=30, choices=OCCASION_CHOICES, default='other')
    chest = models.FloatField(blank=True, null=True)
    waist = models.FloatField(blank=True, null=True)
    hips = models.FloatField(blank=True, null=True)
    shoulder = models.FloatField(blank=True, null=True)
    sleeve_length = models.FloatField(blank=True, null=True)
    garments_length = models.FloatField(blank=True, null=True)
    neck = models.FloatField(blank=True, null=True)
    fabrics = models.ForeignKey(Fabrics, on_delete=models.CASCADE, related_name='custom_orders' , null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.buyer.username} to {self.tailor.business_name}"
