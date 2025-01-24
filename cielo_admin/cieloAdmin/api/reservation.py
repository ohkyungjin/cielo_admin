from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from ..services.reservation_service import ReservationService

@require_http_methods(["POST"])
def create_reservation(request):
    data = json.loads(request.body)
    try:
        reservation = ReservationService.create_reservation(
            pet_data=data['pet'],
            service_id=data['service_id'],
            signature=data['signature']
        )
        return JsonResponse({
            'status': 'success',
            'reservation_id': reservation.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_http_methods(["GET"])
def get_reservation_stats(request):
    stats = ReservationService.get_reservation_stats()
    return JsonResponse(stats)
