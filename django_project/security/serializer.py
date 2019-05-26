from rest_framework import serializers
from django.core.validators import validate_ipv4_address


class EnableSerializer(serializers.Serializer):
    """
    This Serializer defines the expected fields in a Enable security POST Request
    """
    VirtualMachineHostName = serializers.CharField(help_text="Virtual Machine Hostname")
    VirtualMachineIPAddress = serializers.CharField(validators=[validate_ipv4_address],
                                                    help_text="Virtual Machine IP Address")
    VirtualMachineID = serializers.UUIDField(help_text="Virtual Machine ID")
    VirtualMachineRID = serializers.CharField(help_text="Virtual Machine RID")
    TaskID = serializers.CharField(help_text="Unique ID of status response and "
                                             "data payload for success/failure")
    LinuxPolicyID = serializers.CharField(help_text="Policy ID for linux Virtual Machine")
    WindowsPolicyID = serializers.CharField(help_text="Policy ID for windows Virtual Machine")


class DecommissionSerializer(serializers.Serializer):
    """
    This Serializer defines the expected fields in a Decommission security POST Request
    """
    VirtualMachineHostName = serializers.CharField()
    VirtualMachineIPAddress = serializers.CharField(validators=[validate_ipv4_address])
    VirtualMachineID = serializers.UUIDField(help_text="Virtual Machine ID")
    VirtualMachineRID = serializers.CharField(help_text="Virtual Machine RID")
    TaskID = serializers.CharField(help_text="Unique ID of status response and "
                                             "data payload for success/failure")
