from rest_framework import serializers
from django.core.validators import validate_ipv4_address


class EnableVMBackupSerializer(serializers.Serializer):
    """
    This Serializer defines the expected fields in a Enable Backup POST Request
    """
    VirtualMachineHostName = serializers.CharField(help_text="Hostname of target VM")
    VirtualMachineIPAddress = serializers.CharField(validators=[validate_ipv4_address],
                                                    help_text="Virtual Machine IP Address")
    VirtualMachineID = serializers.UUIDField(help_text="Virtual Machine ID")
    VirtualMachineRID = serializers.CharField(help_text="Virtual Machine RID")
    TaskID = serializers.CharField(help_text="Unique ID of status response and data "
                                             "payload for success/failure")
    retentionPeriod = serializers.IntegerField(help_text="Backup retention period (15 or 30)")
    retentionPeriodType = serializers.CharField(help_text="Backup retention period "
                                                          "Type (Days, Weeks, Months or Years)")


class PauseVMBackupSerializer(serializers.Serializer):
    """
    This Serializer defines the expected fields in a Pause Backup POST Request
    """
    VirtualMachineHostName = serializers.CharField(help_text="Hostname of target VM")
    VirtualMachineIPAddress = serializers.CharField(validators=[validate_ipv4_address],
                                                    help_text="Virtual Machine IP Address")
    VirtualMachineID = serializers.UUIDField(help_text="Virtual Machine ID")
    VirtualMachineRID = serializers.CharField(help_text="Virtual Machine RID")
    TaskID = serializers.CharField(help_text="Unique ID of status response and data "
                                             "payload for success/failure")


class DisableVMBackupSerializer(serializers.Serializer):
    """
    This Serializer defines the expected fields in a Disable Backup POST Request
    """
    VirtualMachineHostName = serializers.CharField(help_text="Hostname of target VM")
    VirtualMachineIPAddress = serializers.CharField(validators=[validate_ipv4_address],
                                                    help_text="Virtual Machine IP Address")
    VirtualMachineID = serializers.UUIDField(help_text="Virtual Machine ID")
    VirtualMachineRID = serializers.CharField(help_text="Virtual Machine RID")
    TaskID = serializers.CharField(help_text="Unique ID of status response and data "
                                             "payload for success/failure")


class DecommissionVMBackupSerializer(serializers.Serializer):
    """
    This Serializer defines the expected fields in a Decommission Backup POST Request
    """
    VirtualMachineHostName = serializers.CharField(help_text="Hostname of target VM")
    VirtualMachineIPAddress = serializers.CharField(validators=[validate_ipv4_address],
                                                    help_text="Virtual Machine IP Address")
    VirtualMachineID = serializers.UUIDField(help_text="Virtual Machine ID")
    VirtualMachineRID = serializers.CharField(help_text="Virtual Machine RID")
    TaskID = serializers.CharField(help_text="Unique ID of status response and data "
                                             "payload for success/failure")


class ResumeVMBackupSerializer(serializers.Serializer):
    """
    This Serializer defines the expected fields in a resume Backup POST Request
    """
    VirtualMachineHostName = serializers.CharField(help_text="Hostname of target VM")
    VirtualMachineIPAddress = serializers.CharField(validators=[validate_ipv4_address],
                                                    help_text="Virtual Machine IP Address")
    VirtualMachineID = serializers.UUIDField(help_text="Virtual Machine ID")
    VirtualMachineRID = serializers.CharField(help_text="Virtual Machine RID")
    TaskID = serializers.CharField(help_text="Unique ID of status response and data "
                                             "payload for success/failure")
