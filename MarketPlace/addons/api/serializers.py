from rest_framework import serializers

from addons.models import News, Main, Licence, About


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Main
        fields = '__all__'


class LicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licence
        fields = '__all__'


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'
