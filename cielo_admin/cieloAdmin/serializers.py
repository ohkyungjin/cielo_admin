from rest_framework import serializers
from .models import Reservation

class ReservationCalendarSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name')
    phone = serializers.CharField(source='customer.phone')
    service_name = serializers.CharField(source='service.name')
    pet_name = serializers.CharField(source='pet.name')
    pet_type = serializers.CharField(source='pet.type')
    pet_breed = serializers.CharField(source='pet.breed')
    end_datetime = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['id', 'datetime', 'end_datetime', 'status', 'customer_name', 'phone', 
                 'service_name', 'pet_name', 'pet_type', 'pet_breed']

    def get_end_datetime(self, obj):
        # 예약 시간으로부터 2시간 후를 종료 시간으로 설정
        return obj.datetime + timezone.timedelta(hours=2)
