class Device:
    headings = ['ID', 'Brand', 'Type', 'Serial Number', 'Status']
    fields = {
        '-DeviceID-': 'Device ID:',
        '-Brand-': 'Brand:',
        '-Type-': 'Type:',
        '-SerialNumber-': 'Serial Number:',
        '-Status-': 'Status:'
    }

    def __init__(self, device_id, brand, device_type, serial_number, status):
        self.device_id = device_id
        self.brand = brand
        self.device_type = device_type
        self.serial_number = serial_number
        self.status = status
        self.erased = False  # Added to mark if the record is deleted

    def __eq__(self, other_device):
        return other_device.device_id == self.device_id

    def __str__(self):
        return f"{self.device_id} {self.brand} {self.device_type} {self.serial_number} {self.status}"

    def device_in_pos(self, pos):
        return self.device_id == pos

    def set_device(self, brand, device_type, serial_number, status):
        self.brand = brand
        self.device_type = device_type
        self.serial_number = serial_number
        self.status = status
