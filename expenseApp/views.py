from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee, Vendor, Expense
from .serializers import EmployeeSerializer, VendorSerializer, ExpenseSerializer


@api_view(['GET', 'POST'])
def employee(request):
    if request.method == 'GET':
        try:
            employee_code = request.GET.get('employee_code')
            if employee_code:
                employee_obj = Employee.objects.get(employee_code=employee_code)
            else:
                return Response({'message': 'employee code not passed.'}, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({'message': 'invalid employee code passed.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EmployeeSerializer(employee_obj)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'employee created.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def vendor(request):
    if request.method == 'GET':
        try:
            vendor_code = request.GET.get('vendor_code')
            if vendor_code:
                vendor_obj = Vendor.objects.get(vendor_code=vendor_code)
            else:
                return Response({'message': 'vendor code not passed.'}, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response({'message': 'invalid vendor code passed.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = VendorSerializer(vendor_obj)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'vendor created.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def expense(request):
    serializer = ExpenseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'expense created.'},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def vendor_expense(request):
    try:
        vendor_code = request.GET.get('vendor_code')
        expense_list = Expense.objects.filter(vendor_code=vendor_code)
        serializer = ExpenseSerializer(expense_list, many=True)
        exp_list = []
        for expense_obj in serializer.data:
            employee = Employee.objects.get(employee_code=expense_obj['employee_code'])
            emp_serializer = EmployeeSerializer(employee)
            exp_list.append({
                'employee': emp_serializer.data['name'],
                'expense_made_on': expense_obj['expense_done_on'],
                'expense_comment': expense_obj['expense_comment'],
                'expense_amount': expense_obj['expense_amount']
            })
        response = {
            'name': Vendor.objects.get(vendor_code=vendor_code).name,
            'expenses': exp_list
        }
    except Vendor.DoesNotExist:
        return Response({'message': 'invalid vendor code passed.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(response)


@api_view(['GET'])
def employee_expense(request):
    try:
        employee_code = request.GET.get('employee_code')
        expense_list = Expense.objects.filter(employee_code=employee_code)
        serializer = ExpenseSerializer(expense_list, many=True)
        exp_list = []
        for expense_obj in serializer.data:
            vendor = Vendor.objects.get(vendor_code=expense_obj['vendor_code'])
            ven_serializer = VendorSerializer(vendor)
            exp_list.append({
                'vendor': ven_serializer.data['name'],
                'expense_made_on': expense_obj['expense_done_on'],
                'expense_comment': expense_obj['expense_comment'],
                'expense_amount': expense_obj['expense_amount']
            })
        response = {
            'name': Employee.objects.get(employee_code=employee_code).name,
            'expenses': exp_list
        }
    except Employee.DoesNotExist:
        return Response({'message': 'invalid employee code passed.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(response)