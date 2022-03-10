
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view



schema_view = get_swagger_view(title='Multi_Label_API')


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^api/v1/', include('multi_label_api.urls')),
    url(r'^$', schema_view)

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
