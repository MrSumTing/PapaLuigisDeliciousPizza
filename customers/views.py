from rest_framework import permissions
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
import json

from customers.serializers import CustomerRegisterSerializer, CustomerPreferencesSerializer
from customers.models import CustomerPreferences, Customer


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        print (request.data)

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class CustomerRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print (request.data)
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDataView(APIView):
    def post(self, request):
        try:
            # Get the existing data for the authenticated user
            customer_data = CustomerData.objects.get(customer=request.user)
        except CustomerData.DoesNotExist:
            # If no data exists for this user, create a new record
            customer_data = CustomerData(customer=request.user)

        # Handle pizza order updates
        pizzas_ordered = request.data.get('pizzas_ordered', [])
        for pizza in pizzas_ordered:
            if pizza in customer_data.times_pizza_ordered:
                customer_data.times_pizza_ordered[pizza] += 1
            else:
                customer_data.times_pizza_ordered[pizza] = 1

        # Handle pizza rating updates
        pizzas_ratings = request.data.get('pizzas_ratings', {})
        for pizza, new_rating in pizzas_ratings.items():
            # If the pizza already has a rating, update the average rating
            if pizza in customer_data.avg_pizza_rating:
                current_avg_rating = customer_data.avg_pizza_rating[pizza]
                total_ratings = customer_data.times_pizza_ordered.get(pizza,
                                                                      1)  # Ensure there's at least one order for this pizza
                updated_avg_rating = (current_avg_rating * (total_ratings - 1) + new_rating) / total_ratings
                customer_data.avg_pizza_rating[pizza] = updated_avg_rating
            else:
                # First rating for the pizza
                customer_data.avg_pizza_rating[pizza] = new_rating

        # Save the updated data
        customer_data.save()

        # Serialize the data and return the response
        serializer = CustomerDataSerializer(customer_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerPreferencesView(APIView):
    def get(self, request):
        # Get preferences of the authenticated user
        try:
            preferences = CustomerPreferences.objects.get(user=request.user)
            serializer = CustomerPreferencesSerializer(preferences)

            # Prepare the response
            response_data = {
                'spicy': serializer.data['spicy'],
                'is_vegetarian': serializer.data['is_vegetarian'],
                'is_vegan': serializer.data['is_vegan'],
                'is_meat': serializer.data['is_meat'],
                'is_vegetable': serializer.data['is_vegetable'],
                'cheesy': serializer.data['cheesy'],
                'sweet': serializer.data['sweet'],
                'salty': serializer.data['salty'],
                'budget_range': serializer.data['max_budget'],
                'toppings': []  # Initialize toppings list
            }

            # Populate the toppings list with keys and values
            toppings_keys = [
                'tomato_sauce', 'cheese', 'pepperoni', 'BBQ_sauce', 'chicken',
                'pineapple', 'ham', 'mushrooms', 'olives', 'onions',
                'bacon', 'jalapenos', 'spinach', 'feta_cheese', 'red_peppers',
                'garlic', 'parmesan', 'sausage', 'anchovies', 'basil',
                'broccoli', 'mozzarella', 'ground_beef', 'zucchini',
                'sun_dried_tomatoes'
            ]

            for topping in toppings_keys:
                response_data['toppings'].append({
                    'name': topping,
                    'preference': serializer.data[topping]
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except CustomerPreferences.DoesNotExist:
            return Response(
                {"detail": "Preferences not found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        # Create or update preferences for the authenticated user
        try:
            # Load JSON data from the request body
            data = json.loads(request.body)

            # Extract data
            toppings = data.get('toppings', {})
            spicy = data.get('spicy', 0.5)
            is_meat = data.get('is_meat', 0.5)
            is_vegetable = data.get('is_vegetable', 0.5)
            cheesy = data.get('cheesy', 0.5)
            sweet = data.get('sweet', 0.5)
            salty = data.get('salty', 0.5)
            is_vegetarian = data.get('is_vegetarian', False)
            is_vegan = data.get('is_vegan', False)
            budget_range = data.get('budget_range', 7.00)

            # Update or create user preferences
            preferences, created = CustomerPreferences.objects.update_or_create(
                user=request.user,
                defaults={
                    'spicy': spicy,
                    'is_meat': is_meat,
                    'is_vegetable': is_vegetable,
                    'cheesy': cheesy,
                    'sweet': sweet,
                    'salty': salty,
                    'is_vegetarian': is_vegetarian,
                    'is_vegan': is_vegan,
                    'budget_range': budget_range,
                    # Update toppings from the data
                    **{f"{topping}": toppings.get(topping, 0) for topping in toppings}
                }
            )

            return JsonResponse({'message': 'Preferences updated successfully!'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

class CustomerInfoView(APIView):
    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)

            user_data = {
                'first_name': customer.user.first_name,
                'last_name': customer.user.last_name,
                'email': customer.user.email,
                'address': customer.address_line,
                'postal_code': customer.postal_code,
                'city': customer.city,
            }

            return Response(user_data, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found.'}, status=status.HTTP_404_NOT_FOUND)