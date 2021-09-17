from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework import views
from rest_framework.response import Response

from decimal import Decimal

from .cart import Cart
from .myserializers import CartProductSerializer
from customed_files.rest_framework.rest_framework_customed_classes.custom_rest_authentication import CustomSessionAuthentication 


class CartPageView(views.APIView):       #user come from 'sabad'(in header) to here. 
    def get(self, request, *args, **kwargs):                                       #supose user refresh /cart/ page
        serializers, cart, total_prices = [], Cart(request), Decimal(0)
        for item in cart:
            serializers.append({**CartProductSerializer(item['product'], context={'request': request}).data, 'price': str(item['price']), 'quantity': item['quantity'], 'price_changes': item['price_changes'], 'total_price': str(item['total_price'])})
            total_prices += item['total_price']
        return Response({'sabad': serializers, 'products_count': cart.get_products_count(), 'total_prices': str(total_prices)})



    
class CartMenuView(views.APIView):       #'sabad'(in header)
    def get(self, request, *args, **kwargs):                                       #supose user refresh /cart/ page
        serializers, cart, total_prices = [], Cart(request), Decimal(0)
        for item in cart:
            serializers.append({**CartProductSerializer(item['product'], context={'request': request}).data, 'price': str(item['price']), 'quantity': item['quantity'], 'price_changes': item['price_changes'], 'total_price': str(item['total_price'])})
            total_prices += item['total_price']
        return Response({'sabad': serializers, 'products_count': cart.get_products_count(), 'total_prices': str(total_prices)})



    
class CartAdd(views.APIView):       #user come from 'sabad'(in header) to this method.  add id in front, just front must car add current_item + cart_cookie in add. #set_fingers and remove  is in front 
    def post(self, request, *args, **kwargs):
        #CustomSessionAuthentication().enforce_csrf(request)
        data = request.data
        cart = Cart(request)
        cart.add(product_id=data['product_id'], quantity=data.get('quantity', 1), shopfilteritem_id=data.get('shopfilteritem_id'))    #cd['quantity'] is int but how is it because: coerce=int ? request.data['quantity'] is rest/views/CartDetail is string
        return Response({**CartMenuView().get(request).data})




class CartRemove(views.APIView):       #user come from 'sabad'(in header) to this method.  add id in front, just front must car add current_item + cart_cookie in add. #set_fingers and remove  is in front 
    def post(self, request, *args, **kwargs):
        #CustomSessionAuthentication().enforce_csrf(request)
        cart = Cart(request)
        cart.remove(request.data.get('product_id'))
        return Response({**CartMenuView().get(request).data})
