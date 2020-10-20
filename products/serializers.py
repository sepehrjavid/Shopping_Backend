from rest_framework import serializers

from products.models import Cloth, MultiPicture, CLOTH, SportTool, SPORT_TOOL, Size, Color


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import uuid

        # Check if this is a base64 string
        if isinstance(data, str):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            if file_extension != 'jpg' and file_extension != 'png':
                self.fail('invalid_image')

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class PictureSerializer(serializers.ModelSerializer):
    picture = Base64ImageField()

    class Meta:
        model = MultiPicture
        fields = [
            'id',
            'picture'
        ]


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = [
            'id',
            'size'
        ]


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = [
            'id',
            'name'
        ]


class ClothSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True)
    color_data = serializers.SerializerMethodField()
    size_data = serializers.SerializerMethodField()

    class Meta:
        model = Cloth
        fields = [
            'id',
            'title',
            'price',
            'amount',
            'rating',
            'brand',
            'color',
            'color_data',
            'type',
            'size',
            'size_data',
            'material',
            'pictures'
        ]

        read_only_fields = ('rating', 'id', 'type')
        extra_kwargs = {
            'size': {'write_only': True},
            'color': {'write_only': True},
        }

    def get_size_data(self, obj):
        return SizeSerializer(obj.size.all(), many=True).data

    def get_color_data(self, obj):
        return ColorSerializer(obj.color.all(), many=True).data

    def create(self, validated_data):
        pictures = validated_data.pop('pictures')
        validated_data['type'] = CLOTH
        instance = Cloth.objects.create(**validated_data)
        for picture in pictures:
            MultiPicture.objects.create(picture=picture.get('picture'), product=instance)

        return instance


class SportToolSerializer(serializers.ModelSerializer):
    pictures = PictureSerializer(many=True)
    color_data = serializers.SerializerMethodField()
    size_data = serializers.SerializerMethodField()

    class Meta:
        model = SportTool
        fields = [
            'id',
            'title',
            'price',
            'amount',
            'rating',
            'brand',
            'color_data',
            'color',
            'type',
            'size_data',
            'size',
            'pictures'
        ]

        read_only_fields = ('rating', 'id', 'type')
        extra_kwargs = {
            'size': {'write_only': True},
            'color': {'write_only': True},
        }

    def get_size_data(self, obj):
        return SizeSerializer(obj.size.all(), many=True).data

    def get_color_data(self, obj):
        return ColorSerializer(obj.color.all(), many=True).data

    def create(self, validated_data):
        pictures = validated_data.pop('pictures')
        validated_data['type'] = SPORT_TOOL
        instance = SportTool.objects.create(**validated_data)
        for picture in pictures:
            MultiPicture.objects.create(picture=picture.get('picture'), product=instance)
        return instance
