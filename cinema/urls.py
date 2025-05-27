from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, MovieViewSet, SeatViewSet, BookingViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'seats', SeatViewSet, basename='seat')
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
