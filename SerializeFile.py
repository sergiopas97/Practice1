import csv
import os
from Device import Device

device_file_path = 'Device.csv'

def saveDevice(file_path, oC):
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([oC.device_id, oC.brand, oC.device_type, oC.serial_number, oC.status])
def modifyDevice(file_path, oC):
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Create a temporary file
    temp_file_path = file_path + '.temp'

    with open(file_path, 'r', newline='') as input_file, open(temp_file_path, 'w', newline='') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file)

        for row in reader:
            existing_object = Device(*row)

            # Check if this is the object to modify
            if existing_object.posFile == oC.posFile:
                # Write the modified object to the output file
                writer.writerow([oC.device_id, oC.brand, oC.device_type, oC.serial_number, oC.status])
            else:
                # Write the unchanged object to the output file
                writer.writerow(row)

    # Replace the original file with the modified file
    os.remove(file_path)
    os.rename(temp_file_path, file_path)


def readDevice(file_path, lC):
    lC.clear()  # Borra la lista existente
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                device = Device(*row)
                lC.append(device)
