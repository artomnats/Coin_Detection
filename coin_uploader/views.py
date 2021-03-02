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
        average_color = open_cv_image.mean(axis=0).mean(axis=0)
        # Convert RGB to BGR
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        gray_img = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        width, height = img.width, img.height

        img = cv2.medianBlur(gray_img, 7)
        circles = cv2.HoughCircles(
            img, cv2.HOUGH_GRADIENT, 1, 50, param1=100,
            param2=50, minRadius=10, maxRadius=380,
        )
        circles = numpy.round(circles[0, :]).astype("int")
        coin_count = {
            1: 0,
            2: 0,
            5: 0,
            10: 0,
        }
        if circles is None:
            circles = []
        number_of_circles = 0
        for (x, y, r) in circles:
            number_of_circles += 1
            if r < 75:
                coin_count[1] += 1
            elif r > 85:
                coin_count[5] += 1
            elif r >= 80:
                coin_count[2] += 1
            else:
                coin_count[10] += 1
        sum_of_coins = sum([i*j for i, j in coin_count.items()])
        result = {
            "number_of_coins": number_of_circles,
            "average_color": tuple(average_color),
            "coins": coin_count,
            "total_sum": sum_of_coins,
            "width": width,
            "height": height,
        }
        return result
