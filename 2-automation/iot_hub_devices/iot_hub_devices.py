# This module is used to create and manage devices in Azure IoT Hub
import pulumi
import subprocess
import yaml
import json

# TODO: define device class and add methods to the devices. Get device (should return a code for existing).

def adding_devices_based_on_yaml(iot_hub_name):
    """
    Adds devices to the specified IoT Hub based on the device list in the yaml file.

    Args:
        hub_name (str): The name of the IoT Hub.

    Raises:
        Exception: If the Azure CLI command fails for any reason.
    """
    if pulumi.runtime.is_dry_run():
        # Skip execution during preview (dry run)
        pulumi.log.info("Skipping adding devices to IoT Hub during preview.")
        return []

    # Read in the yaml file
    with open("device-list.yaml", 'r') as f:
        try:
            devices = yaml.safe_load(f)
            # print("Devices: ", devices)
        except yaml.YAMLError as exc:
            print(exc)

    connection_strings = []
    for country in devices:
        for device in devices[country]:
            # Check if the device is already existing
            command = f"az iot hub device-identity show --hub-name {iot_hub_name} --device-id {device['name']}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Device {device['name']} already exists.")
                continue
            else:
                print(f"Adding device: {device['name']}")
                connection_string = create_edge_device(device['name'], iot_hub_name)
                connection_strings.append(connection_string)

    return connection_strings

def create_edge_device(device_id, iot_hub_name):
    """
    Adds a taxi device to the specified IoT Hub using the Azure CLI.

    Args:
        hub_name (str): The name of the IoT Hub.
        device_id (str): The unique identifier for the IoT device to be created.

    Raises:
        Exception: If the Azure CLI command fails for any reason.

    Returns:
        Tuple[str, str]: The device ID and primary key for the newly created device.
    """
    try:
        command = f"az iot hub device-identity create --hub-name {iot_hub_name} --device-id {device_id} --edge-enabled"
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        device_info = json.loads(result.stdout)
        primary_key = device_info["authentication"]["symmetricKey"]["primaryKey"]
        return device_id, primary_key

    except subprocess.CalledProcessError as e:
        raise Exception(f"Failed to add device {device_id}: {e}")