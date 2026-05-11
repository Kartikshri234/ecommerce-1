"""Order & Payment Views"""
import logging
import razorpay
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from shop.models import Order

logger = logging.getLogger(__name__)


@login_required
def order_success(request, order_id):
    """Display order success page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_success.html", {"order": order})


@login_required
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})


@login_required
def razorpay_checkout(request, order_id):
    """Initiate Razorpay payment for an order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.payment_method != 'razorpay':
        messages.error(request, "Invalid payment method for this order")
        return redirect('order_detail', order_id=order.id)
    
    # Initialize Razorpay client
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
    
    # Create payment order
    razorpay_order = client.order.create(
        amount=int(float(order.total_amount) * 100),  # Amount in paise
        currency='INR',
        receipt=f'order_{order.id}',
    )
    
    context = {
        'order': order,
        'razorpay_order': razorpay_order,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
    }
    
    return render(request, 'razorpay_payment.html', context)


@login_required
@csrf_exempt
def razorpay_callback(request):
    """Handle Razorpay payment callback"""
    if request.method == 'POST':
        try:
            payment_details = {
                'razorpay_order_id': request.POST.get('razorpay_order_id', ''),
                'razorpay_payment_id': request.POST.get('razorpay_payment_id', ''),
                'razorpay_signature': request.POST.get('razorpay_signature', ''),
            }
            
            # Validate required fields
            if not all(payment_details.values()):
                logger.error(f"Missing payment details for user {request.user.id}")
                messages.error(request, "Invalid payment response from Razorpay")
                return redirect('cart')
            
            # Verify payment signature
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            client.utility.verify_payment_signature(payment_details)
            
            # Update order status
            order_id = request.POST.get('order_id')
            if not order_id:
                logger.error("Order ID missing from payment callback")
                messages.error(request, "Order ID not found in payment response")
                return redirect('cart')
            
            try:
                order = Order.objects.get(id=order_id, user=request.user)
            except Order.DoesNotExist:
                logger.error(f"Order {order_id} not found for user {request.user.id}")
                messages.error(request, "Order not found")
                return redirect('cart')
            
            order.status = 'processing'
            order.save()
            
            messages.success(request, "Payment successful! ✅")
            return redirect('order_success', order_id=order.id)
        
        except razorpay.BadRequestsError as e:
            logger.error(f"Razorpay error for user {request.user.id}: {str(e)}")
            messages.error(request, f"Payment verification failed: Invalid signature")
            return redirect('cart')
        except Exception as e:
            logger.error(f"Unexpected error in razorpay_callback for user {request.user.id}: {str(e)}")
            messages.error(request, f"Payment failed: An unexpected error occurred")
            return redirect('cart')
