from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.utils.timezone import now
from .models import Room, Movie, Seat, Booking
from .serializers import RoomSerializer, MovieSerializer, SeatSerializer, BookingSerializer
import logging

logger = logging.getLogger(__name__)

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        try:
            room_id = self.request.query_params.get('room')
            upcoming = self.request.query_params.get('upcoming')

            if room_id:
                room_ids = [rid.strip() for rid in room_id.split(',')]
                valid_room_ids = []
                for rid in room_ids:
                    try:
                        valid_room_ids.append(int(rid))
                    except (ValueError, TypeError):
                        logger.warning(f"Ignoring invalid room_id value: {rid}")

                if valid_room_ids:
                    queryset = queryset.filter(room_id__in=valid_room_ids)
                else:
                    logger.info("No valid room IDs provided; returning empty queryset.")
                    return queryset.none()

            if upcoming is not None:
                upcoming_lower = upcoming.lower()
                if upcoming_lower == 'true':
                    queryset = queryset.filter(start_time__gte=now())
                elif upcoming_lower == 'false':
                    queryset = queryset.filter(start_time__lt=now())
                else:
                    logger.warning(f"Invalid 'upcoming' parameter value: {upcoming}")

        except Exception as e:
            logger.error(f"Unexpected error in get_queryset: {e}", exc_info=True)
            return self.queryset.none()

        return queryset

class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset

        room_id = self.request.query_params.get('room')
        if room_id:
            try:
                room_id = int(room_id)
                queryset = queryset.filter(room_id=room_id)
            except ValueError:
                logger.warning(f"Invalid room ID in query params: {room_id}")
                raise ValidationError({"room": "Room ID must be an integer."})

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        movie_id = self.request.query_params.get('movie')
        if movie_id:
            try:
                int(movie_id)
            except ValueError:
                logger.warning(f"Invalid movie ID in query params: {movie_id}")
                raise ValidationError({"movie": "Movie ID must be an integer."})

        context['movie_id'] = movie_id
        return context

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('seat', 'movie', 'seat__room')
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        seat = request.data.get('seat')
        movie = request.data.get('movie')
        if Booking.objects.filter(seat_id=seat, movie_id=movie).exists():
            return Response({'error': 'Seat already booked for this movie.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def booked_seats(self, request):
        room_id = request.query_params.get('room')

        if not room_id:
            return Response({'error': 'room parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            room_id = int(room_id)
        except ValueError:
            return Response({'error': 'room ID must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        movies = Movie.objects.filter(room_id=room_id)

        if not movies.exists():
            return Response({'error': 'No movies found for this room'}, status=status.HTTP_404_NOT_FOUND)

        response_data = []

        for movie in movies:
            bookings = self.queryset.filter(movie=movie).select_related('seat')
            seats = [{'row': b.seat.row, 'number': b.seat.number} for b in bookings]

            response_data.append({
                'movie_id': movie.id,
                'movie_title': movie.title,
                'start_time': movie.start_time,
                'booked_seats': seats
            })

        return Response(response_data)

    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        bookings = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)