from django.shortcuts import render

# Create your views here.
def reserve(request):
	return render(request,'reserve/reservation.html')
