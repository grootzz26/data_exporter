from django.shortcuts import render
from .models import *
from .serializers import common_serializer
from rest_framework.response import Response
from django.views.decorators.http import require_http_methods
from rest_framework.generics import ListAPIView
from .helpers import write_list_of_dict_to_excel
import requests
from django.http.response import JsonResponse


# @require_http_methods(['GET'])
# def get_customers_data(request):
#     pass
class CustomerListAPIView(ListAPIView):

    def list(self, request, *args, **kwargs):
        serialize = common_serializer(Customers, "__all__")(Customers.objects.all(), many=True)
        # path = write_list_of_dict_to_excel([serialize.data], source='Customers')
        return Response(serialize.data)


@require_http_methods(["GET"])
def export_source_data(request, src):
    breakpoint()
    model = eval(src)
    serialize = common_serializer(model, "__all__")(model.objects.all(), many=True)
    breakpoint()
    write_list_of_dict_to_excel([serialize.data], source='Customers')
    return JsonResponse(
        {
            "status": 200,
            "message": f"{src} data is exported "
        }
    )


class ExportedFilesListAPIView(ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response(
            common_serializer(ExportDataLogs, "__all__")(ExportDataLogs.objects.all(), many=True).data
        )
