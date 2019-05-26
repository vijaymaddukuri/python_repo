from rest_framework import serializers
from django.core.validators import validate_ipv4_address

class EnableLogForwarderSerializer(serializers.Serializer):
    """
    This Serializer defines the expected fields in a Enable Log Forwarder POST Request.
    """
    VirtualMachineHostName = serializers.CharField(help_text="Virtual Machine Hostname")
    VirtualMachineIPAddress = serializers.CharField(validators=[validate_ipv4_address],
                                                    help_text="Virtual Machine IP Address")
    VirtualMachineID = serializers.UUIDField(help_text="Virtual Machine ID")
    VirtualMachineRID = serializers.CharField(help_text="Virtual Machine RID")
    TaskID = serializers.CharField(help_text="Unique ID of status response and data "
                                             "payload for success/failure")
