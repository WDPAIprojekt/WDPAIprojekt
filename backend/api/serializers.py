# from rest_framework import serializers
# from .models import SystemUser, Budget, Expense

# class RegisterSerializer(serializers.ModelSerializer):
#     """
#     Serializer do rejestracji użytkownika systemowego.
#     """
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = SystemUser
#         # fields = ['username', 'password'] 


#     def create(self, validated_data):
#         user = SystemUser.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password']
#         )
#         return user

# class ExpenseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Expense
#         fields = ['id', 'name', 'amount']

# class BudgetSerializer(serializers.ModelSerializer):
#     expenses = ExpenseSerializer(many=True)

#     class Meta:
#         model = Budget
#         fields = ['id', 'total_amount', 'expenses']

#     def create(self, validated_data):
#         expenses_data = validated_data.pop('expenses')
#         budget = Budget.objects.create(**validated_data)
#         for expense_data in expenses_data:
#             Expense.objects.create(budget=budget, **expense_data)
#         return budget


from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from .models import SystemUser, Budget, Expense

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer do rejestracji użytkownika systemowego.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = SystemUser
        fields = ['username', 'password'] 


    def create(self, validated_data):
        user = SystemUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer dla modelu Expense (Wydatek).
    """
    class Meta:
        model = Expense
        fields = ['id', 'name', 'amount']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

class BudgetSerializer(serializers.ModelSerializer):
    """
    Serializer dla modelu Budget (Budżet).
    """
    expenses = ExpenseSerializer(many=True, required=False)

    class Meta:
        model = Budget
        fields = ['id', 'total_amount', 'expenses']

    def create(self, validated_data):
        user = self.context["request"].user
        expenses_data = validated_data.pop('expenses', [])  # Domyślnie pusta lista, gdy brak wydatków
        budget = Budget.objects.create(user=user, **validated_data)
        for expense_data in expenses_data:
            Expense.objects.create(budget=budget, **expense_data)
        return budget

    def update(self, instance, validated_data):
        # expenses_data = validated_data.pop('expenses', [])
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.save()

        # Aktualizacja wydatków
        # instance.expenses.all().delete()  # Usuwamy istnieące wydatki
        # for expense_data in expenses_data:
        #     Expense.objects.create(budget=instance, **expense_data)

        return instance

    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Total amount must be greater than 0.")
        return value
