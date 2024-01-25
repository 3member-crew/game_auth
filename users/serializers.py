from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            'password': {'write_only':True}
        }
    
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        instance.score = validated_data.get('score')
        instance.save()
        return instance