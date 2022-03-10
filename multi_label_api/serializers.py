from rest_framework import serializers


class MultiLabelSerializer(serializers.Serializer):
    path_of_folder = serializers.CharField()