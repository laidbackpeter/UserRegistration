# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import authentication
from authentication import KeyAuth as custom_authentication
from serializers import RegisterFarmerRequestSerializer, RegisterSeedBagRequestSerializer
from models import Farmers, SeedBag
from structlog import get_logger

# Create your views here.


class RegisterFarmer(APIView):
    """End point to register a farmer

        Response
        ========
        202 [Accepted]  Request accepted processing underway
        400 [Bad Request] Malformed request
        403 [Forbidden] API authentication failed

        Sample JSON request data
        =======================
        {
            "first_name" : "Peter",
            "last_name" : "Muchina",
            "other_name" : "Ndegwa",
            "phone_number" : "254725817350",
            "country" : "Kenya",
            "langauge" : "Swahili",
            "district" : "Nairobi",
            "village" : "Tipis",
            "crop" : "Potatoes"
        }

    """
    authentication_classes = (
        authentication.SessionAuthentication, custom_authentication
    )

    def post(self, request):
        """
        :param request:
        :return:
        """
        logger = get_logger(__name__)

        try:
            request_payload = request.data
            logger.info('register_farmer_request', request_payload=request_payload)
            serializer = RegisterFarmerRequestSerializer(data=request_payload)
            if serializer.is_valid():
                farmer_model = Farmers(
                    first_name=request_payload['first_name'],
                    last_name=request_payload['last_name'],
                    other_name=request_payload.get('other_name', None),
                    phone_number=request_payload['phone_number'],
                    country=request_payload['country'],
                    language=request_payload['language'],
                    district=request_payload['district'],
                    village=request_payload['village'],
                    crop=request_payload['crop'],
                )
                farmer_model.save()
                response = {"Details": "Ok"}
                logger.info(
                    'register_farmer_response', response=response,
                    status=status.HTTP_202_ACCEPTED)
                return Response(status=status.HTTP_202_ACCEPTED, data=response)
            else:
                logger.info(
                    'register_farmer_response', response=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        except Exception as e:
            logger.info(
                'register_farmer_response', response=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(data="Opps!!! Something went wrong",
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )


class RegisterSeedBag(APIView):
    """End point to register a farmer

        Response
        ========
        202 [Accepted]  Request accepted processing underway
        400 [Bad Request] Malformed request
        403 [Forbidden] API authentication failed

        Sample JSON request data
        =======================
        {
            "phone_number" : "254725817350",
            "bag_unique_number" : "12345ygft"
        }

    """
    authentication_classes = (
        authentication.SessionAuthentication, custom_authentication
    )

    def post(self, request):
        """
        :param request:
        :return:
        """
        logger = get_logger(__name__)

        try:
            request_payload = request.data
            logger.info('register_seed_bag_request', request_payload=request_payload)
            serializer = RegisterSeedBagRequestSerializer(data=request_payload)
            if serializer.is_valid():
                phone_number = request_payload['phone_number']
                try:
                    farmer = Farmers.objects.get(phone_number=phone_number)
                except Farmers.DoesNotExist:
                    farmer = False

                if farmer:
                    seed_bag_model = SeedBag(
                        farmer=farmer,
                        bag_unique_number=request_payload['bag_unique_number']
                    )
                    seed_bag_model.save()
                    response = {"Details": "Ok"}
                    logger.info(
                        'register_seed_bag_response', response=response,
                        status=status.HTTP_202_ACCEPTED)
                    return Response(status=status.HTTP_202_ACCEPTED, data=response)
                else:
                    response = {"Details": "Farmer doesn't exists"}
                    logger.info(
                        'register_seed_bag_response', response=response,
                        status=status.HTTP_202_ACCEPTED)
                    return Response(status=status.HTTP_202_ACCEPTED, data=response)
            else:
                logger.info(
                    'register_seed_bag_response', response=serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        except Exception as e:
            logger.info(
                'register_seed_bag_response', response=str(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(data="Opps!!! Something went wrong",
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )
