import pulumi
import pulumi_azure_native as an

# Showcase a class setup for the Key Vault

class KeyVault:
    def __init__(self, environment: str, name: str, resource_group_name: str, location: str, tags: dict, tenant: str, opts: pulumi.ResourceOptions = None):
        # Check which environment we are operating iin
        if environment == "dev":
            # Create the Azure Key Vault
            self.key_vault = an.keyvault.Vault(name,
                                                vault_name = name,
                                                resource_group_name = resource_group_name,
                                                location = location,
                                                properties = an.keyvault.VaultPropertiesArgs(
                                                    sku = an.keyvault.SkuArgs(
                                                        family = "A",
                                                        name = "standard"
                                                    ),
                                                    tenant_id = tenant,
                                                    enable_rbac_authorization = True,
                                                ),
                                               tags = tags)

        elif environment == "prod":
            # Create the Azure Key Vault
            self.key_vault = an.keyvault.Vault(name,
                                                vault_name=name,
                                                resource_group_name = resource_group_name,
                                                location = location,
                                                properties = an.keyvault.VaultPropertiesArgs(
                                                    sku = an.keyvault.SkuArgs(
                                                        family = "A",
                                                        name = "premium"
                                                    ),
                                                    tenant_id = tenant,
                                                    enable_rbac_authorization = True,
                                                ),
                                                tags = tags)
        else:
            raise ValueError(f"Unknown environment: {environment}")

        # Expose outputs
        self.name = self.key_vault.name
        self.id = self.key_vault.id

    @classmethod
    def from_output(
        cls,
        environment: str,
        name: str,
        resource_group_name: pulumi.Output[str],
        location: pulumi.Output[str],
        tags: dict,
        tenant: str,
        opts: pulumi.ResourceOptions = None,
    ):
        """
        Alternative constructor to handle Pulumi Output[str] for dynamic inputs.
        """
        def create_key_vault(args):
            name_val, rg_val, loc_val, tags_val, tenant_val = args
            return cls(
                environment,
                name=name_val,
                resource_group_name=rg_val,
                location=loc_val,
                tags=tags_val,
                tenant=tenant_val,
                opts=opts,
            )

        return pulumi.Output.all(name, resource_group_name, location, tags, tenant).apply(create_key_vault)





