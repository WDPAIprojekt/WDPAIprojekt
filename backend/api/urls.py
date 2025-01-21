from django.urls import path, re_path
from .views import register, current_user, create_budget, get_budgets, delete_expense, create_or_update_expense, update_budget
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# from .views import TestView

app_name="api"
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('current_user/', current_user, name='current_user'),
    path('budget/create/', create_budget, name='create_budget'),
    path('budget/list/', get_budgets, name='get_budgets'),
    path('budget/update/', update_budget, name='update_budget'),
    path('expense/delete/<int:expense_id>/', delete_expense, name='delete_expense'),
    re_path(r'^create_or_update_expense(?:/(?P<expense_id>\d+))?/?$', 
            create_or_update_expense, 
            name='create_or_update_expense'),
]
# from django.urls import path
# from .views import (
#     register,
#     current_user,
#     create_budget,
#     get_budgets,
#     add_expense_to_budget,
#     get_expenses_for_budget,
# )
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

# app_name = "api"

# urlpatterns = [
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('register/', register, name='register'),
#     path('current_user/', current_user, name='current_user'),
#     path('budget/create/', create_budget, name='create_budget'),
#     path('budget/list/', get_budgets, name='get_budgets'),
#     path('budget/<int:budget_id>/expense/add/', add_expense_to_budget, name='add_expense_to_budget'),
#     path('budget/<int:budget_id>/expenses/', get_expenses_for_budget, name='get_expenses_for_budget'),
# ]
