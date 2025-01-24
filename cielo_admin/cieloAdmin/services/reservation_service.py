from ..models.reservation import Reservation, Pet, Service

class ReservationService:
    @staticmethod
    def create_reservation(pet_data, service_id, signature):
        # 반려동물 정보 생성
        pet = Pet.objects.create(**pet_data)
        
        # 서비스 조회
        service = Service.objects.get(id=service_id)
        
        # 예약 생성
        reservation = Reservation.objects.create(
            pet=pet,
            service=service,
            status='pending',
            total_price=service.base_price,
            signature=signature
        )
        
        return reservation

    @staticmethod
    def get_reservation_stats():
        return {
            'total': Reservation.objects.count(),
            'pending': Reservation.objects.filter(status='pending').count(),
            'confirmed': Reservation.objects.filter(status='confirmed').count(),
            'completed': Reservation.objects.filter(status='completed').count(),
            'cancelled': Reservation.objects.filter(status='cancelled').count(),
        }
