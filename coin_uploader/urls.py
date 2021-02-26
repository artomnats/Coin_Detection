try:
    import sys
    from django.urls import re_path
    from coin_uploader.views import ImageProcessView
except ImportError as exception:
    print("%s - Exception from file\n \
%s - Please install the necessary libraries." % (__file__, exception))
    sys.exit(0)

urlpatterns = [
    re_path('.*$(?i)', ImageProcessView.as_view(template_name='upload.html'), name='coin_counter'),

]
