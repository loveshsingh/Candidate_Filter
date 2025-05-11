from django.shortcuts import render
from .models import Testimonial

def testimonials_page(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'testimonial/testimonials.html', {'testimonials': testimonials})
