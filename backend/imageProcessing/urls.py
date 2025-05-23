from django.urls import path
from .views import upload_files
from django.conf import settings
from django.conf.urls.static import static
from .views import CheckImageHashView, SaveImageHashView

urlpatterns = [

    path('upload/', upload_files, name='upload_files'),
    path('check-image-hash/', CheckImageHashView.as_view(), name='check-image-hash'),
    path('save-image-hash/', SaveImageHashView.as_view(), name='save-image-hash'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
