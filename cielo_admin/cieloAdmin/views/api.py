from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models.reservation import Reservation
from ..serializers import ReservationCalendarSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reservation_calendar(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    status = request.GET.get('status')
    service = request.GET.get('service')

    # 기본 쿼리셋
    queryset = Reservation.objects.all()

    # 날짜 필터링
    if start:
        queryset = queryset.filter(datetime__gte=start)
    if end:
        queryset = queryset.filter(datetime__lte=end)

    # 상태 필터링
    if status and status != 'all':
        queryset = queryset.filter(status=status)

    # 서비스 필터링
    if service and service != 'all':
        queryset = queryset.filter(service_id=service)

    # 정렬
    queryset = queryset.order_by('datetime')

    # 시리얼라이즈
    serializer = ReservationCalendarSerializer(queryset, many=True)
    return Response(serializer.data)
