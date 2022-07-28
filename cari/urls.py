from django.urls import path
from .views import ResultDetail, UserInfo, SendEmail
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('cari/image', UserInfo.as_view(), name='cari_image'),
    path('cari/result', ResultDetail.as_view(), name='cari_result'),
    path('cari/email', SendEmail.as_view(), name='cari_email')
]

# image conversion
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)