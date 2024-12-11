import pulumi, os, utils
import pulumi_azure_native as an
from iot_hub_devices import adding_devices_based_on_yaml
from key_vault import KeyVault

# TODO: Usually there would be a SP for the Pulumi Automation
# TODO: Create utils function for naming conventions

# ------------------------------------------------------------------ Init Config and ENV variables ------------------------------------------------------------------

# Initialize Config for your project
config = pulumi.Config("azure-native")
location = config.get("location") or "West Europe"

# Get ENV variables (mostly secrets) from environment variables
principal_id = os.getenv("AZURE_CLIENT_ID")
tenant_id = os.getenv("AZURE_TENANT_ID")
env = os.getenv("ENVIRONMENT")

# Verify env. Must be either "dev" or "prod"
if env not in ["dev", "prod"]:
    raise ValueError(f"Unknown environment: {env}")

# ------------------------------------------------------------------        Resource groups        ------------------------------------------------------------------
resource_group = an.resources.ResourceGroup("rg-fb-sit-tmp",
                                            resource_group_name="rg-fb-sit-tmp",
                                            location = location,
                                            tags = utils.get_tags(env))


# ------------------------------------------------------------------        Resources              ------------------------------------------------------------------
# Create Azure Key Vault for storing the connection strings
key_vault = KeyVault.from_output(env, "kv-fb-sit-tmp", resource_group.name, resource_group.location, utils.get_tags(env), tenant_id)

# Create the IoT Hub
iot_hub = an.devices.IotHubResource("iothub-fb-sit-tmp",
                                    resource_group_name = resource_group.name,
                                    location = resource_group.location,
                                    sku = an.devices.IotHubSkuInfoArgs(
                                        name = "F1",
                                        capacity = 1),
                                    properties = an.devices.IotHubPropertiesArgs(event_hub_endpoints={}),
                                    tags = utils.get_tags(env))

# Add devices to the IoT Hub
connection_strings = iot_hub.name.apply(adding_devices_based_on_yaml)

# ------------------------------------------------------------------        Governance            ------------------------------------------------------------------
# Key Vault Administrator for the Pulumi Service Principal (me)
role_assignment_kv_pulumi_sp =  an.authorization.RoleAssignment("role-assignment-kv-pulumi-sp", principal_id=principal_id, role_definition_id="/providers/Microsoft.Authorization/roleDefinitions/00482a5a-887f-4fb3-b363-3b7fe8e74483", scope=key_vault.key_vault.id)



