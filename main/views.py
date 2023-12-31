from django.shortcuts import render
from . import serializers
from . import models
from rest_framework import generics, permissions, pagination, viewsets
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# Create your views here.
 
class VendorList(generics.ListCreateAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    # permission_classes = [permissions.IsAuthenticated]
    

    def perform_create(self, serializer):
        return super().perform_create(serializer)

class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    # permission_classes = [permissions.IsAuthenticated]

class ProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.GET.get('category')  # Utilisation de get() avec une valeur par défaut None

        if category_id:
            try:
                category = models.ProductCategory.objects.get(id=category_id)
                qs = qs.filter(category=category)
            except models.ProductCategory.DoesNotExist:
                pass  # Gérer la catégorie inexistante ici, si nécessaire

        return qs

class TagProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        tag=self.kwargs['tag']
        qs = qs.filter(tags=tag)
        return qs 


class RelatedProductList(generics.ListCreateAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        product_id=self.kwargs['pk']
        product = models.Product.objects.get(id=product_id)
        qs = qs.filter(category = product.category).exclude(id=product_id)
        return qs 

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class CustomerList(generics.ListCreateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerSerializer

@csrf_exempt
def customer_login(request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)


        if user:
            msg={
                'bool':True,
                'user':user.username
            }
        else:
             msg={
                'bool':False,
                'msg':'Invalid Username or Password'
            }
        return JsonResponse(msg)

@csrf_exempt
def customer_register(request):
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')

        try:
            existing_user = User.objects.filter(username=username).exists()
            existing_mobile = models.Customer.objects.filter(mobile=mobile).exists()

            if existing_user:
                msg={
                    'bool':False,
                    'msg':'Username already exist !!!'
                }
            elif existing_mobile:
                 msg={
                    'bool':False,
                    'msg':'Mobile already exist !!!'
                    }
            else:
                user = User.objects.create(
                    first_name=firstname,
                    last_name=lastname, 
                    username=username,
                    email=email,
                    password=password,
                )
                
                # Create customer
                customer = models.Customer.objects.create(
                    user=user,
                    mobile=mobile,
                    )
                msg={
                    'bool':True,
                    'user':user.id,
                    'customer':customer.id,
                    'msg':"Thank you for youregistartion. Please login",
                 }
               
        except IntegrityError:
                msg={
                        'bool':False,
                        'msg':'Ooop something went wrong'
                    }

        return JsonResponse(msg)
class OrderList(generics.ListCreateAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

class OrderDetail(generics.ListAPIView):
    # queryset = models.Order.objects.all()
    serializer_class = serializers.OrderDetailSerializer
    def get_queryset(self):
        orderId = self.kwargs['pk']

        order = models.Order.objects.get(id=orderId)
        order_items = models.OrderItem.objects.filter(order=order)

        return order_items

class OrderItemList(generics.ListCreateAPIView):
    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)

class OrderItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer


class CustomerAddressViewSet(viewsets.ModelViewSet):
    queryset = models.CustomerAddress.objects.all()
    serializer_class= serializers.CustomerAddressSerializer

    # def get_queryset(self):
    #     customer_id = self.kwargs['pk']
    #     customer = models.Customer.objects.get(id=customer_id)
    #     customer_addresses = models.CustomerAddress.objects.filter(customer=customer)
    #     return customer_addresses

class ProductRatingViewSet(viewsets.ModelViewSet):
    queryset = models.ProductRating.objects.all()
    serializer_class= serializers.ProductRatingSerializer



class CategoryList(generics.ListCreateAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.CategorySerializer
    # pagination_class= pagination.LimitOffsetPagination 

    def perform_create(self, serializer):
        return super().perform_create(serializer)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProductCategory.objects.all()
    serializer_class = serializers.CategorySerializer