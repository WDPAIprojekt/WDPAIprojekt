from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, ExpenseSerializer
from .models import Budget, Expense
from .serializers import BudgetSerializer
from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='post',
    operation_description='Umożliwia rejestracje użytkowników.',
    responses={
        201: openapi.Response('Pomyślnie utworzono użytkownika.'),
        400: openapi.Response('Nieprawidłowe dane wejściowe.')
    }
)
@api_view(['POST'])  # Rejestracja dostępna publicznie
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED  # Pomyślnie utworzono użytkownika
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST  # Nieprawidłowe dane wejściowe
    )
    # TODO: Return another error code for user existing

@swagger_auto_schema(
    method='get',
    operation_description='Zwraca nazwę użytkownika aktualnie zalogowanego.',
    responses={
        200: openapi.Response('Zwraca username zalogowanego użytkownika.')
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = request.user
    return Response({
        'username': user.username,
    })

@swagger_auto_schema(
    method='post',
    operation_description="Tworzy nowy budżet na podstawie danych dostarczonych w żądaniu.",
    responses={
        201: openapi.Response('Pomyślnie utworzono budżet.'),
        400: openapi.Response('Nieprawidłowe dane wejściowe.')
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_budget(request):
    serializer = BudgetSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@swagger_auto_schema(
    method='get',
    operation_description="Pobiera listę wydatków w danym budżecie zalogowanego użytkownika.",
    responses={
        200: openapi.Response('Lista budżetów.')
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_budgets(request):
    budgets = Budget.objects.prefetch_related('expenses').filter(user=request.user)
    serializer = BudgetSerializer(budgets, many=True)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )

@swagger_auto_schema(
    method='delete',
    operation_description="Usuwa wydatek o podanym ID, należący do zalogowanego użytkownika.",
    responses={
        204: openapi.Response('Pomyślnie usunięto wydatek.'),
        404: openapi.Response('Nie znaleziono wydatku.')
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, budget__user=request.user)

    expense.delete()

    return Response(
        status=status.HTTP_204_NO_CONTENT
    )

@swagger_auto_schema(
    method='patch',
    operation_description="Częściowa aktualizacja budżetu użytkownika. "
                          "Jeśli budżet nie istnieje, zostaje utworzony.",
    responses={
        204: openapi.Response('Pomyślnie zaktualizowano lub utworzono budżet.'),
        400: openapi.Response('Nieprawidłowe dane wejściowe.'),
    }
)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_budget(request):
    budget, _ = Budget.objects.get_or_create(user=request.user)
    serializer = BudgetSerializer(budget, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
    return Response(
        status=status.HTTP_204_NO_CONTENT,
    )
    
@swagger_auto_schema(
    method='post',
    operation_description="Tworzy lub aktualizuje wydatek. "
                          "Jeśli podany `expense_id` istnieje, wydatek jest aktualizowany, "
                          "w przeciwnym razie tworzony jest nowy.",
    responses={
        200: openapi.Response('Pomyślnie zaktualizowano wydatek.'),
        201: openapi.Response('Pomyślnie utworzono wydatek.'),
        400: openapi.Response('Nieprawidłowe dane wejściowe.'),
        500: openapi.Response('Błąd serwera.')
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_or_update_expense(request, expense_id=None):
    try:
        # Find or create a single budget for this user
        # E.g. assume each user has exactly 1 budget
        budget, _ = Budget.objects.get_or_create(user=request.user)

        expense = Expense.objects.filter(id=expense_id, budget__user=request.user).first()

        if expense:
            serializer = ExpenseSerializer(expense, data=request.data, partial=True)
            if serializer.is_valid():
                # Force the same budget for updates
                serializer.save(budget=budget)  
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)

        else:
            serializer = ExpenseSerializer(data=request.data)
            if serializer.is_valid():
                # Assign budget and create a new expense
                serializer.save(budget=budget)
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

# Stworzyć nowy view dla dodawania expenses
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_expense(request):
    
