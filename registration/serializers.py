from rest_framework import serializers


class RegisterFarmerRequestSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50, label="First name", required=True)
    last_name = serializers.CharField(max_length=50, label="Last name", required=True)
    other_name = serializers.CharField(max_length=50, label="Other name", allow_blank=True)
    phone_number = serializers.CharField(max_length=20, label="Phone Number", required=True, )
    country = serializers.CharField(max_length=50, label="Country", required=True)
    district = serializers.CharField(max_length=50, label="District", required=True)
    village = serializers.CharField(max_length=50, label="Village", required=True)
    crop = serializers.CharField(max_length=50, label="Crop", required=True)


class RegisterSeedBagRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, label="Phone Number", required=True, )
    bag_unique_number = serializers.CharField(max_length=50, label="Bag Unique Number",
                                              required=True)
