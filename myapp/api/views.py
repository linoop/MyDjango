from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from myapp.models import Product
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from . serializers import ProductSerializers, UserSerializers
from django.contrib.auth import authenticate

from myapp.api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/products',
    ]
    return Response(routes)


@api_view(['POST'])
def createUser(request):
    if request.method == 'POST':
        serializers = UserSerializers(data=request.data)
        context = {}
        if serializers.is_valid():
            user = serializers.save()
            context['status'] = True
            context['message'] = 'User created successfully'
            # context['user'] = serializers.data
            context['token'] = Token.objects.create(user=user).key
        else:
            context['status'] = False
            context['message'] = f'{serializers.errors}'
        return Response(context)


class UserLogin(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        context = {}
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        email = request.data['email']
        password = request.data['password']
        account = authenticate(email=email, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            context['status'] = True
            context['message'] = 'Successfully authenticated'
            context['id'] = account.pk
            context['email'] = email
            context['token'] = token.key
        else:
            context['status'] = False
            context['message'] = f'Invalid credentials {email, password}'
            context['id'] = 0
            context['email'] = email
            context['token'] = ''
        return Response(context)


class ProductManager(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        req = request.data['req']
        resp = {}
        if req == 'name':
            names = [product.name for product in Product.objects.all()]
            resp['status'] = True
            resp['message'] = 'Success'
            resp['names'] = names
        elif req == 'all':
            products = Product.objects.all()
            serializer = ProductSerializers(products, many=True)
            resp['status'] = True
            resp['message'] = 'Success'
            resp['products'] = serializer.data
        elif req == 'product':
            pk = request.data['pk']
            product = Product.objects.filter(pk=pk)
            if not product:
                resp['status'] = False
                resp['message'] = 'Product data not available'
            else:
                serializer = ProductSerializers(product, many=True)
                resp['status'] = True
                resp['message'] = 'Success'
                resp['products'] = serializer.data        
        return Response(resp)
    
    def post(self, request):
        resp = {}
        product = request.data
        serializer = ProductSerializers(data=product)
        if serializer.is_valid():
            serializer.save()
            resp['status'] = True
            resp['message'] = 'Successfully saved'
            resp['product'] = serializer.data
        else:
            resp['status'] = False
            resp['message'] = 'Wrong data received'
        return Response(resp)
    
    def put(self, request):
        resp = {}
        pk = request.data['id']
        product = request.data
        product_instance = Product.objects.get(id=pk)
        serializer = ProductSerializers(instance=product_instance, data=product)
        if serializer.is_valid():
            serializer.save()
            resp['status'] = True
            resp['message'] = 'Successfully updated'
            resp['product'] = serializer.data
        else:
            resp['status'] = False
            resp['message'] = 'Wrong data received'
        return Response(resp)
    
    def delete(self, request):
        resp = {}
        pk = request.data['id']
        product = Product.objects.filter(id=pk)
        if product:
            product.delete()
            resp['status'] = True
            resp['message'] = 'Successfully deleted'
        else:
            resp['status'] = False
            resp['message'] = 'Product not found'
        return Response(resp)
            
