from rest_framework import serializers
from .models import Room, Movie, Seat, Booking

class RoomSerializer(serializers.ModelSerializer):
    total_seats = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = '__all__'

    def get_total_seats(self, obj):
        return obj.seats.count()

class MovieSerializer(serializers.ModelSerializer):
    room_name = serializers.CharField(source='room.name', read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    is_booked = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = '__all__'

    def get_is_booked(self, obj):
        movie_id = self.context.get('movie_id')
        if not movie_id:
            return False
        return Booking.objects.filter(seat=obj, movie_id=movie_id).exists()

class BookingSerializer(serializers.ModelSerializer):
    seat_info = serializers.SerializerMethodField()
    movie_title = serializers.CharField(source='movie.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user']

    def get_seat_info(self, obj):
        return {
            'row': obj.seat.row,
            'number': obj.seat.number,
            'room': obj.seat.room.name
        }