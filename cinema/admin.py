from django.contrib import admin
from .models import Room, Movie, Seat, Booking


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class MovieInline(admin.TabularInline):
    model = Movie
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "room", "start_time")
    list_filter = ("room", "start_time")
    search_fields = ("title",)
    date_hierarchy = "start_time"
    autocomplete_fields = ("room",)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("room", "row", "number")
    list_filter = ("room", "row")
    search_fields = ("row", "number")
    ordering = ("room", "row", "number")
    autocomplete_fields = ("room",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("seat", "movie", "booked_at")
    list_filter = ("movie", "booked_at")
    search_fields = ("seat__row", "seat__number", "movie__title")
    autocomplete_fields = ("seat", "movie")
