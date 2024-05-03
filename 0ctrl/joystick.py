import os
import struct
import array
from fcntl import ioctl
import threading

# Define axis and button mappings
def get_axis_map(num_axes, buf):
    axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'z',
    0x03 : 'rx',
    0x04 : 'ry',
    0x05 : 'rz',
    0x06 : 'trottle',
    0x07 : 'rudder',
    0x08 : 'wheel',
    0x09 : 'gas',
    0x0a : 'brake',
    0x10 : 'lr',
    0x11 : 'fb',
    0x12 : 'hat1x',
    0x13 : 'hat1y',
    0x14 : 'hat2x',
    0x15 : 'hat2y',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
    0x18 : 'pressure',
    0x19 : 'distance',
    0x1a : 'tilt_x',
    0x1b : 'tilt_y',
    0x1c : 'tool_width',
    0x20 : 'volume',
    0x28 : 'misc',
}
    axis_map = []
    for axis in buf[:num_axes]:
        axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
        axis_map.append(axis_name)
    return axis_map

def get_button_map(num_buttons, buf):
    button_names = {
    0x120 : 'trigger',
    0x121 : 'thumb',
    0x122 : 'thumb2',
    0x123 : 'top',
    0x124 : 'top2',
    0x125 : 'pinkie',
    0x126 : 'base',
    0x127 : 'base2',
    0x128 : 'base3',
    0x129 : 'base4',
    0x12a : 'base5',
    0x12b : 'base6',
    0x12f : 'dead',
    0x130 : 'a',
    0x131 : 'b',
    0x132 : 'c',
    0x133 : 'x',
    0x134 : 'y',
    0x135 : 'z',
    0x136 : 'tl',
    0x137 : 'tr',
    0x138 : 'tl2',
    0x139 : 'tr2',
    0x13a : 'select',
    0x13b : 'start',
    0x13c : 'mode',
    0x13d : 'thumbl',
    0x13e : 'thumbr',
 
    0x220 : 'dpad_up',
    0x221 : 'dpad_down',
    0x222 : 'dpad_left',
    0x223 : 'dpad_right',
 
    0x2c0 : 'dpad_left',
    0x2c1 : 'dpad_right',
    0x2c2 : 'dpad_up',
    0x2c3 : 'dpad_down',
}
    button_map = []
    for btn in buf[:num_buttons]:
        btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
        button_map.append(btn_name)
    return button_map

# Function to read joystick input
def read_joystick():
    print('Available devices:')
    for fn in os.listdir('/dev/input'):
        if fn.startswith('js'):
            print('  /dev/input/%s' % (fn))

    # Open the joystick device
    fn = '/dev/input/js0'
    print('Opening %s...' % fn)
    jsdev = open(fn, 'rb')

    # Get the device name
    buf = array.array('B', [0] * 64)
    ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf)  # JSIOCGNAME(len)
    js_name = buf.tobytes().rstrip(b'\x00').decode('utf-8')
    print('Device name: %s' % js_name)

    # Get number of axes and buttons
    buf = array.array('B', [0])
    ioctl(jsdev, 0x80016a11, buf)
    num_axes = buf[0]

    buf = array.array('B', [0])
    ioctl(jsdev, 0x80016a12, buf)
    num_buttons = buf[0]

    # Get axis and button mappings
    buf = array.array('B', [0] * 0x40)
    ioctl(jsdev, 0x80406a32, buf)  # JSIOCGAXMAP
    axis_map = get_axis_map(num_axes, buf)

    buf = array.array('H', [0] * 200)
    ioctl(jsdev, 0x80406a34, buf)  # JSIOCGBTNMAP
    button_map = get_button_map(num_buttons, buf)

    print('%d axes found: %s' % (num_axes, ', '.join(axis_map)))
    print('%d buttons found: %s' % (num_buttons, ', '.join(button_map)))

    while True:
        evbuf = jsdev.read(8)
        if evbuf:
            time, value, type, number = struct.unpack('IhBB', evbuf)

            if type & 0x80:
                print("(initial)", end="")

            if type & 0x01:
                button = button_map[number]
                if button:
                    print(button)

            if type & 0x02:
                axis = axis_map[number]
                if axis:
                    print(axis, value / 32767.0)

if __name__ == "__main__":
    joystick_thread = threading.Thread(target=read_joystick)
    joystick_thread.daemon = True
    joystick_thread.start()
    # Do other initialization or tasks here, the joystick thread will continue running in the background
