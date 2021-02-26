try:
    import os
    import sys

    import cv2
    import numpy
    from PIL import Image

    from django.shortcuts import render
    from django.views.generic import TemplateView
    from django.utils.decorators import method_decorator
    from django.views.decorators.csrf import csrf_exempt
except ImportError as exception:
    print("%s - Exception from file\n \
%s - Please install the necessary libraries." % (__file__, exception))
    sys.exit(0)



@method_decorator(csrf_exempt, name='dispatch')
class ImageProcessView(TemplateView):
    """
    Upload image.
    Detect cyrcles and get coins size.
    """
    template_name = 'result.html'
    __max_file_size = 1024*1024*16

    def post(self, request):
        """
        Upload image
        Args:
            request - user input.
        Return:
            coins
        """
        my_file = request.FILES.get('file')
        if my_file is None:
            result = {"error": "No file has been received"}
        elif my_file.size > ImageProcessView.__max_file_size:
            result = {"error": "File is too big"}
        else:
            try:
                result = self.__process_image(my_file)
            except Exception as e:
                result = {
                    "error": str(e)
                }
                print(e)
            print(result)
        context = {**result}
        return render(request, ImageProcessView.template_name, context=context)

    def __process_image(self, file):

        try:
            img = Image.open(file)
            open_cv_image = numpy.array(img)
        except Exception:
            raise RuntimeError("Failed to parse an image from the file")
        if open_cv_image.ndim != 3:
            raise RuntimeError("Image is not three dimensional, or is not colored image")
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        grayimg = cv2.cvtColor(open_cv_image, cv2.cv2.COLOR_BGR2GRAY)
        width, height = img.width, img.height

        blurred = cv2.GaussianBlur(grayimg, (7, 7), 0)

        circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=2.2, minDist=100,
                                   param1=200, param2=100, minRadius=50, maxRadius=120)
        number_of_circles = circles.size
        average_color = open_cv_image.mean(axis=0).mean(axis=0)
        result = {
            "number_of_coins": number_of_circles,
            "average_color": tuple(average_color),
            "width": width,
            "height": height,
        }
        return result
