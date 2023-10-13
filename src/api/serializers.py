from rest_framework.serializers import (HyperlinkedModelSerializer, SerializerMethodField, PrimaryKeyRelatedField)
from django.contrib.auth import get_user_model
from appeals.models import (Appeal, Category)


class AppealSerializer(HyperlinkedModelSerializer):
    """Appeal serializer"""
    creator = SerializerMethodField(read_only=True)
    def get_creator(self, obj):
        return obj.creator.get_full_name()
    
    category = SerializerMethodField(read_only=False)
    def get_category(self, obj):
        return obj.category.id
    
    assigned_to = SerializerMethodField(read_only=True)
    def get_assigned_to(self, obj):
        return obj.assigned_to.get_full_name() if obj.assigned_to else ''
    
    class Meta:
        model = Appeal
        fields = '__all__'


class AppealListSerializer(HyperlinkedModelSerializer):
    
    creator = SerializerMethodField(read_only=True)

    def get_creator(self, obj):
        return obj.creator.get_full_name()
    
    #category for appeal
    category = PrimaryKeyRelatedField(many=False, queryset=Category.objects.all(), read_only=False)
    
    # add Id for creator in
    # creator = PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = Appeal
        fields = ['id', 'title', 'text', 'category', 'creator', 'updated_at', 'url', 'app_status']
        depth = 1


class UserListSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = ('id','email', 'password', 'name', 'second_name', 'phone', 'url', 'rank')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', '')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))
        return super().update(instance, validated_data)
    
class UserSerializer(HyperlinkedModelSerializer):
    creator_appeals_set = AppealSerializer(many=True, read_only=True)
    assigned_appeals_set = AppealSerializer(many=True, read_only=True)
    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = ('id','email', 'password', 'name', 'second_name', 'phone', 'url', 'rank', 'creator_appeals_set', 'assigned_appeals_set')
        extra_kwargs = {'password': {'write_only': True}}
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))
        return super().update(instance, validated_data)


class CategorySerializer(HyperlinkedModelSerializer):
    appeals = AppealSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ('url', 'name', 'appeals')
