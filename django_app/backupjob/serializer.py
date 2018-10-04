from rest_framework import serializers


class BackupSerializer(serializers.Serializer):
    TenantID = serializers.UUIDField()
    VirtualMachineID = serializers.UUIDField()
    VirtualMachineHostName = serializers.CharField()
    RetentionDays = serializers.IntegerField()
    Callback = serializers.CharField()
