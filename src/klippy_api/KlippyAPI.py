import requests

class KlippyAPI:
    def __init__(self, base_url):
        """
        Initialize the Klippy API client.

        :param base_url: Base URL of the Klippy server (e.g., http://hostname:port).
        """
        self.base_url = base_url

    def get_printer_info(self):
        """
        Get Klippy host information.

        :return: JSON response containing printer info.
        """
        url = f"{self.base_url}/printer/info"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def emergency_stop(self):
        """
        Trigger an emergency stop.

        :return: Response text (should be 'ok').
        """
        url = f"{self.base_url}/printer/emergency_stop"
        response = requests.post(url)
        response.raise_for_status()
        return response.text

    def restart_host(self):
        """
        Restart the Klippy host.

        :return: Response text (should be 'ok').
        """
        url = f"{self.base_url}/printer/restart"
        response = requests.post(url)
        response.raise_for_status()
        return response.text

    def firmware_restart(self):
        """
        Restart the Klippy firmware.

        :return: Response text (should be 'ok').
        """
        url = f"{self.base_url}/printer/firmware_restart"
        response = requests.post(url)
        response.raise_for_status()
        return response.text

    def list_printer_objects(self):
        """
        List available printer objects.

        :return: JSON response containing available printer objects.
        """
        url = f"{self.base_url}/printer/objects/list"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def query_printer_object_status(self, query_params):
        """
        Query the status of specific printer objects.

        :param query_params: A dictionary of objects and their specific parameters to query.
                             Example: {"gcode_move": None, "toolhead": None, "extruder": "target,temperature"}
        :return: JSON response containing object statuses.
        """
        query_string = "&".join(
            f"{key}={value}" if value else f"{key}" for key, value in query_params.items()
        )
        url = f"{self.base_url}/printer/objects/query?{query_string}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

# Example usage:
if __name__ == "__main__":
    base_url = "http://192.168.31.100:7125"
    klippy = KlippyAPI(base_url)

    try:
        # Get printer info
        printer_info = klippy.get_printer_info()
        print("Printer Info:", printer_info)

        # List printer objects
        printer_objects = klippy.list_printer_objects()
        print("Printer Objects:", printer_objects)

        # Query printer object status
        status = klippy.query_printer_object_status({"gcode_move": None, "toolhead": None, "extruder": "target,temperature"})
        print("Printer Status:", status)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
