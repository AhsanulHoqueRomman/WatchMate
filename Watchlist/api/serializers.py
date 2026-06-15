from rest_framework import serializers

from Watchlist.models import WatchList, StreamPlatform, Review



#Below are the serializer class:

'''

def name_length(value):
    if len(value) > 30 :
        raise serializers.ValidationError('Name is too long')
    else:
        return value

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only =True)
    name = serializers.CharField(validators =[name_length])
    description = serializers.CharField()
    active = serializers.BooleanField()
    
    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
      
#There are 3 types of validations:

#Field Level Validation :
#Syntaxt:
# def validate_<field_name>(self, value):
#     # validation logic
#     return value


    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Name is too short')
        else:
            return value
  
        
#Object level validation: Works wiithin an object of database.
#Syntax:
# def validate(self, data):
#     validation logic
#     return data

    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError('Name and Description can not be same!')
        else:
            return data
        
#Validators: Validators are reusable validation functions or classes that can be attached directly to serializer fields.
# They are useful when the same validation logic is needed in multiple serializers.

#syntax :
# field_name = serializers.CharField(validators=[validator_function])
# def validator_function(value):
    # validation logic
    # return value
    
    
'''

#Now here is the ModelSerializer classes:

'''
class MovieSerializer(serializers.ModelSerializer):
    
    len_of_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = '__all__'
        # fields = '__all__'
        # fields = ('id', 'name', 'description')
        # exclude = ('active')        #all the fields are included except active field.
        
    def get_len_of_name(self, object):
        length = len(object.name)
        return length
        
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError('Name is too short')
        else:
            return value
        
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError('Name and Description can not be same!')
        else:
            return data
            
            
'''

# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = '__all__'



# class WatchListSerializer(serializers.HyperlinkedModelSerializer):
# class WatchListSerializer(serializers.ModelSerializer):    
#     reviews = ReviewSerializer(many=True, read_only=True)
#     class Meta:
#         model = WatchList
#         fields = '__all__'
        
        
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    # watchlist = serializers.StringRelatedField(many=True)
    # watchlist = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # watchlist = serializers.HyperlinkedRelatedField(many=True,read_only=True, view_name='WatchDetailsAV')
    
    class Meta:
        model = StreamPlatform
        fields = '__all__'