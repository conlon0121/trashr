from rest_framework import serializers


class IntervalReadingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    raw_reading = serializers.IntegerField(required=True)
    percent_capacity = serializers.DecimalField(max_digits=5, decimal_places=2)
    timestamp = serializers.DateTimeField()
    # Pass the id of the dumpster
    dumpster_id = serializers.ReadOnlyField(source='dumpster', read_only=True)

    def create(self, validated_data):
        dumpster = Dumpster.objects.get(id=validated_data['dumpster'])
        percent_capacity = dumpster.capacity / validated_data['raw_reading']

        return IntervalReading.objects.create(
            raw_reading=validated_data['raw_reading'],
            percent_capacity=percent_capacity,
            dumpster=dumpster
        )
