# Currently unused class because I fucked up
# May be used in the future, however
# TODO: Delete or use
from trashr.models import Dumpster
from trashr.models import IntervalReading
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class IntervalReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalReading
        fields = ('raw_reading', 'timestamp', 'dumpster')

    def create(self, validated_data):
        dumpster = Dumpster.objects.filter(id=self.initial_data['dumpster'])
        if dumpster.exists():
            dumpster = dumpster.get()
        else:
            raise ValidationError("Dumpster Does not exist")
        # Find how full the dumpster is based on the raw reading
        percent_capacity = dumpster.capacity / (dumpster.capacity - validated_data.get('raw_reading'))
        reading = IntervalReading.objects.update_or_create(
            raw_reading=validated_data.get('raw_reading'),
            percent_capacity=percent_capacity,
            timestamp=validated_data.get('timestamp'),
            dumpster=dumpster
        )[0]
        return reading
