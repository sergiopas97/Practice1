from SerializeFile import *
from Device import *  # Assuming you have a Device class defined
import PySimpleGUI as sg
import operator
import os
import re

device_file_path = 'Device.dat'

fDevice = open(device_file_path, 'rb+')  # Change the filename to match your device data file
lDevice = []
pattern_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
pattern_ID = r"\d{3}"
pattern_phone = r"\d{3}-\d{6}"

# Verifica si el archivo existe y créalo si no existe
if not os.path.exists(device_file_path):
    with open(device_file_path, 'wb'):
        pass

fDevice = open(device_file_path, 'rb+')


def addDevice(l_Device, t_DeviceInterfaz, oDevice):
    # Lógica de validación
    valida = True

    # Validación del ID
    if not oDevice.device_id:
        sg.popup_error('Error', 'Device ID is required.')
        valida = False
    elif any(device.device_id == oDevice.device_id for device in l_Device):
        sg.popup_error('Error', 'Device ID is already in use. Please choose a different one.')
        valida = False

    # Validación del resto de los campos
    if not oDevice.brand:
        sg.popup_error('Error', 'Brand is required.')
        valida = False

    if not oDevice.device_type:
        sg.popup_error('Error', 'Device Type is required.')
        valida = False

    if not oDevice.serial_number:
        sg.popup_error('Error', 'Serial Number is required.')
        valida = False
    elif not re.match(pattern_phone, oDevice.serial_number):
        sg.popup_error('Error', 'Invalid Serial Number format. It must be in the format "###-######".')
        valida = False

    if not oDevice.status:
        sg.popup_error('Error', 'Status is required.')
        valida = False

    # Agregar el dispositivo si la validación es exitosa
    if valida:
        l_Device.append(oDevice)
        saveDevice(device_file_path, oDevice)
        t_DeviceInterfaz.append(
            [oDevice.device_id, oDevice.brand, oDevice.device_type, oDevice.serial_number, oDevice.status])


def delDevice(l_Device, t_DeviceInterfaz, selected_rows):
    selected_positions = [t_DeviceInterfaz[row][-1] for row in selected_rows]

    devices_to_remove = []
    for o in l_Device:
        if o.serial_number in selected_positions:  # Modifica esto según tu lógica
            devices_to_remove.append(o)

    for device in devices_to_remove:
        l_Device.remove(device)

    # Elimina todas las filas correspondientes a los dispositivos seleccionados
    t_DeviceInterfaz = [row for row in t_DeviceInterfaz if row[-1] not in selected_positions]

    return t_DeviceInterfaz
def updateDevice(l_Device, t_row_DeviceInterfaz, posinFile):
    cdel = None
    for o in l_Device:
        if o.device_in_pos(posinFile):
            cdel = o
            break
    if cdel is not None:
        cdel.set_device(t_row_DeviceInterfaz[1], t_row_DeviceInterfaz[2], t_row_DeviceInterfaz[3],
                        t_row_DeviceInterfaz[4])
        modifyDevice(fDevice, cdel)


def sort_table(table, cols):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table


def interfaz():
    font1, font2 = ('Arial', 14), ('Arial', 16)
    sg.theme('LightGrey1')  # Change the theme to a light theme
    sg.set_options(font=font1)
    table_data = []
    rowToUpdate = []
    readDevice(device_file_path, lDevice)

    for o in lDevice:
        if not o.erased:
            table_data.append([o.device_id, o.brand, o.device_type, o.serial_number, o.status])

    layout = [
                 [sg.Push(), sg.Text('Device CRUD', font=font2), sg.Push()],
             ] + [
                 [sg.Text(text, font=font1), sg.Push(), sg.Input(key=key, font=font1)] for key, text in
                 Device.fields.items()
             ] + [
                 [sg.Push()] +
                 [sg.Button(button, size=(10, 1), font=font1) for button in ('Add', 'Delete', 'Modify', 'Clear')] +
                 [sg.Push()],
                 [sg.Table(values=table_data, headings=Device.headings, max_col_width=50, num_rows=10,
                           display_row_numbers=False, justification='center', enable_events=True,
                           enable_click_events=True,
                           vertical_scroll_only=False, select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                           # Cambiado a 'EXTENDED'
                           expand_x=True, bind_return_key=True, key='-Table-', font=font1)],
                 [sg.Button('Purge', font=font1), sg.Push(), sg.Button('Sort File', font=font1)],
             ]

    window = sg.Window('Device Management with Files', layout, finalize=True)
    window['-PosFile-'].update(disabled=True)
    window['-Table-'].bind("<Double-Button-1>", " Double")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Add':
            # Lógica de validación
            valida = True  # Actualiza a True si la validación es exitosa

            if valida:
                addDevice(
                    lDevice,
                    table_data,
                    Device(
                        values['-DeviceID-'],
                        values['-Brand-'],
                        values['-Type-'],
                        values['-SerialNumber-'],
                        values['-Status-']
                    )
                )
                window['-Table-'].update(table_data)
        if event == 'Delete':
            if len(values['-Table-']) > 0:
                selected_rows = values['-Table-']
                table_data = delDevice(lDevice, table_data, selected_rows)
                window['-Table-'].update(table_data)

        if event == '-Table- Double':
            if len(values['-Table-']) > 0:
                row = values['-Table-'][0]
                window['-DeviceID-'].update(disabled=True)
                window['-DeviceID-'].update(str(table_data[row][0]))
                window['-Brand-'].update(str(table_data[row][1]))
                window['-Type-'].update(str(table_data[row][2]))
                window['-SerialNumber-'].update(str(table_data[row][3]))
                window['-Status-'].update(str(table_data[row][4]))

        if event == 'Clear':
            window['-DeviceID-'].update(disabled=False)
            window['-DeviceID-'].update('')
            window['-Brand-'].update('')
            window['-Type-'].update('')
            window['-SerialNumber-'].update('')
            window['-Status-'].update('')

        if event == 'Modify':
            valida = False
            # Add validation logic for Device attributes if needed
            if valida:
                for t in table_data:
                    if t[-1] == int(values['-PosFile-']):
                        rowToUpdate = t
                        t[1], t[2], t[3], t[4] = values['-Brand-'], values['-Type-'], values['-SerialNumber-'], values[
                            '-Status-']
                        break
                updateDevice(lDevice, rowToUpdate, int(values['-PosFile-']))
                window['-Table-'].update(table_data)
                window['-DeviceID-'].update(disabled=False)



        if isinstance(event, tuple):
            print(event)
            print(values)

        if event[0] == '-Table-':
            if event[2][0] == -1:
                col_num_clicked = event[2][1]
                table_data = sort_table(table_data, (col_num_clicked, 0))
                window['-Table-'].update(table_data)

    window.close()


interfaz()
fDevice.close()
