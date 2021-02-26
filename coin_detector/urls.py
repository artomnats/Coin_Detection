try:
    import sys
    from django.contrib import admin
    from django.urls import path, re_path, include
except ImportError as exception:
    print("%s - Exception from file\n \
%s - Please install the necessary libraries." % (__file__, exception))
    sys.exit(0)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('coin_uploader.urls')),
]
