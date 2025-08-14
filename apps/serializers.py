from rest_framework import serializers

class CommonSerializers(serializers.ModelSerializer):
    def run_validation(self, data=serializers.empty):
        try:
            return super().run_validation(data)
        except serializers.ValidationError as exc:
            first_error = list(exc.detail.items())[0]
            field, messages = first_error
            raise serializers.ValidationError({field: [messages[0]]})