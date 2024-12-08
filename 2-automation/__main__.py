import pulumi
from pulumi_azure_native import resources
from pulumi_azure_native import devices
from iot_hub_devices import adding_devices_based_on_yaml

# Initialize Config for your project
config = pulumi.Config("azure-native")
location = config.get("location") or "West Europe"

# Global tags
tags = {
    "environment": "dev",
    "owner": "Fabian Brünger",
}

# Create an Azure Resource Group
resource_group = resources.ResourceGroup("rg-fb-sit-tmp",
                                            resource_group_name="rg-fb-sit-tmp",
                                            location = location)

# Create Azure Key Vault for storing the connection strings
# TODO: Create Key Vault

# Create the IoT Hub
iot_hub = devices.IotHubResource("iothub-fb-sit-tmp",
                                    resource_group_name = resource_group.name,
                                    location = resource_group.location,
                                    sku = devices.IotHubSkuInfoArgs(
                                        name = "F1",
                                        capacity = 1),
                                    properties = devices.IotHubPropertiesArgs(event_hub_endpoints={}),
                                    tags = tags)

# Add devices to the IoT Hub
connection_strings = iot_hub.name.apply(adding_devices_based_on_yaml)


