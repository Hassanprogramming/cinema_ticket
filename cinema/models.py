from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    poster = models.ImageField(upload_to="posters/")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="movies")
    start_time = models.DateTimeField()

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.title} at {self.start_time.strftime('%H:%M')}"


class Seat(models.Model):
    row = models.IntegerField()
    number = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="seats")

    class Meta:
        unique_together = ("row", "number", "room")
        ordering = ["room", "row", "number"]

    def __str__(self):
        return f"Row {self.row} Seat {self.number}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("seat", "movie")
        ordering = ["-booked_at"]
