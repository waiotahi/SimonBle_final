from jnius import autoclass, cast, JavaException, PythonJavaClass, java_method
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.clock import Clock, mainthread
from functools import partial
from kivy.utils import platform
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.config import Config
import re 
Config.set('input', 'keyboard', 'system')

if platform == 'android':
    print('Device is android')

    from android.runnable import run_on_ui_thread

    BluetoothProfile = autoclass('android.bluetooth.BluetoothProfile')
    BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
    BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
    BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
    BluetoothGatt = autoclass('android.bluetooth.BluetoothGatt')
    BluetoothGattCallback = autoclass(
        'android.bluetooth.BluetoothGattCallback')
    BluetoothGattCharacteristic = autoclass(
        'android.bluetooth.BluetoothGattCharacteristic')
    BluetoothGattService = autoclass('android.bluetooth.BluetoothGattService')
    BluetoothGattDescriptor = autoclass(
        'android.bluetooth.BluetoothGattDescriptor')
    BluetoothLeScanner = autoclass('android.bluetooth.le.BluetoothLeScanner')

    ScanCallback = autoclass('android.bluetooth.le.ScanCallback')
    ScanResult = autoclass('android.bluetooth.le.ScanResult')
    Context = autoclass('android.content.Context')
    PythonScanCallback = autoclass('org.kivy.ble.PythonScanCallback')
    CallbackWrapper = autoclass('org.kivy.ble.CallbackWrapper')
    PythonBluetoothGattCallback = autoclass(
        'org.kivy.ble.PythonBluetoothGattCallback')
    BluetoothGattCallBackWrapper = autoclass(
        'org.kivy.ble.BluetoothGattCallBackWrapper')
    UUID = autoclass('java.util.UUID')

    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    Intent = autoclass('android.content.Intent')
    AndroidString = autoclass('java.lang.String')
    Toast = autoclass('android.widget.Toast')
    JavaClass = autoclass('java.lang.Class')
    IntegerClass = autoclass('java.lang.Integer')
    context = PythonActivity.mActivity.getApplicationContext()
    mActivity = PythonActivity.mActivity

    @run_on_ui_thread
    def show_toast(text='Hello'):
        context = PythonActivity.mActivity
        text_char_sequence = cast(
            'java.lang.CharSequence', AndroidString(text))
        duration = Toast.LENGTH_SHORT
        toast = Toast.makeText(context, text_char_sequence, duration)
        toast.show()


# My Device ids
SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = '0000ffe1-0000-1000-8000-00805f9b34fb'
DESCRIPTOR_UUID = '00002902-0000-1000-8000-00805f9b34fb'


#DEVICE_MAC = "8D:3C:82:19:5F:7C"
DEVICE_MAC = "94:A9:A8:34:30:72"
####################################


# SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"

# CHARACTERISTIC_UUID = "00002902-0000-1000-8000-00805f9b34fb"

# DESCRIPTOR_UUID = "00002901-0000-1000-8000-00805f9b34fb"

#DEVICE_MAC = "94:A9:A8:34:30:72"

REQUEST_ENABLE_BT = 1


class PScanCallback(PythonJavaClass):
    __javacontext__ = 'app'
    __javainterfaces__ = ["org/kivy/ble/CallbackWrapper"]

    def __init__(self, callback):
        print("scan calll", callback)
        self.callback = callback
        #self._scanner = scanner
        #self.java = defs.PythonScanCallback(self)

    @java_method("(I)V")
    def onScanFailed(self, errorCode):
        print('from error code', errorCode)

    @java_method("(Landroid/bluetooth/le/ScanResult;)V")
    def onScanResult(self, result):
        #print('from on resukt')

        print('from on resukt', result)
        self.callback(result)


class PythonBluetoothGattCallbackInterface(PythonJavaClass):

    __javacontext__ = 'app'
    __javainterfaces__ = ["org/kivy/ble/BluetoothGattCallBackWrapper"]

    def __init__(self, connection_state_change=None,
                 services_discovered=None, characteristic_changed=None, characteristic_read=None,
                 characteristic_write=None, mtu_changed=None):
        self.connection_state_change = connection_state_change
        self.mtu_changed = mtu_changed
        self.services_discovered = services_discovered
        self.characteristic_changed = characteristic_changed
        self.characteristic_read = characteristic_read

    @java_method("(II)V")
    def onConnectionStateChange(self, status, new_state):
        #print('=== onConnectionStateChange ')
        if self.connection_state_change:
            self.connection_state_change(status, new_state)

    @java_method("(II)V")
    def onMtuChanged(self, mtu, status):
        print("==== onMtuChanged", mtu, status)
        if self.mtu_changed:
            self.mtu_changed(mtu, status)

    @java_method("(I)V")
    def onServicesDiscovered(self, status):
        print("==== onServicesDiscovered", status)
        if self.services_discovered:
            self.services_discovered(status)

    @java_method("(I[B)V")
    def onCharacteristicChanged(self, handle, value):
        # ba=AndroidString(value).getBytes("UTF-8")
        # python_byte_array = bytearray(ba)
        # ps=python_byte_array.decode("utf-8")
        # print(ps)
        print("=== onCharacteristicChanged", handle, value)
        if self.characteristic_changed:
            self.characteristic_changed(handle, value)

    @java_method("(II[B)V")
    def onCharacteristicRead(self, handle, status, value):
        print("=== onCharacteristicRead", handle, status, value)
        if self.characteristic_read:
            self.characteristic_read(handle, status, value)

    @java_method("(II)V")
    def onCharacteristicWrite(self, handle, status):
        print("=== onCharacteristicWrite",)
        if self.characteristic_write:
            self.characteristic_write(handle, status)

    @java_method("(Ljava/lang/String;I[B)V")
    def onDescriptorRead(self, uuid, status, value):
        print("== onDescriptorRead")

    @java_method("(Ljava/lang/String;I)V")
    def onDescriptorWrite(self, uuid, status):
        print("== onDescriptorWrite")


class MainScreen(BoxLayout):
    obj = ObjectProperty(None)
    bar = False
    testing = False
    event = None
    bluetoothGatt = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_key_down=self.on_key_down)
        self.running = False

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        # F12 key code is 293
        if key == 293 or key in (13, 271):
            self._record(key)
        return True

    def _record(self, *args):
        #print("Enter key ",args)
        self.ids.input_box.text = self.ids.output_label.text


    @mainthread
    def _update_ui(self, *args):
        #print(args)
        self.ids.output_label.text = str(args[0])

    @mainthread
    def _update_status(self,*args):
        self.ids.status_label.text = args[0] 

    def _start(self):
        self.connect_ble()

    def _stop(self):
        self.disconnect_ble()
        self._update_status("Not Reading ...")

    def connectToDevice(self, context, device):
        self.pbci = PythonBluetoothGattCallbackInterface(self.connection_state_change,
                                                         self.services_discovered, self.characteristic_changed)
        self.bgc = PythonBluetoothGattCallback(self.pbci)
        print(self.bgc)
        self.bluetoothGatt = device.connectGatt(context, False, self.bgc)

    def stop_call(self, *args):
        print("_stop_call ", args)

    def services_discovered(self, status):
        # if status==BluetoothGatt.GATT_SUCCESS:
        print("Gatt sucess")
        service = self.bluetoothGatt.getService(UUID.fromString(SERVICE_UUID))
        print(service)
        if service:
            characteristic = service.getCharacteristic(
                UUID.fromString(CHARACTERISTIC_UUID))
            print(characteristic)
            self.bluetoothGatt.setCharacteristicNotification(
                characteristic, True)
            descriptor = characteristic.getDescriptor(
                UUID.fromString(DESCRIPTOR_UUID))
            print(descriptor)
            if descriptor:
                descriptor.setValue(
                    BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE)
                self.bluetoothGatt.writeDescriptor(descriptor)
                show_toast("Notification On")

    def emg_changed(self, data):
        if data:
            print("Byte Array data ", data)
            decoded_data = data.decode('utf-8',errors='ignore').strip()
            print(decoded_data)
            # Accumulate BLE fragments
            if not hasattr(self, "_ble_buffer"):
                self._ble_buffer = ""
            self._ble_buffer += decoded_data
            # Process only when full message received (ends with '0000' or newline)
            if self._ble_buffer.endswith("0000") or "\n" in self._ble_buffer:
                # Extract weight using regex
                match = re.search(r'([\d.]+)\s*kg', self._ble_buffer)
                if match:
                    weight = float(match.group(1))
                    print("Weight:", weight)
                    # Update only the clean numeric weight in UI
                    self._update_ui(f"{weight:.3f}")
                else:
                    print("No valid weight found:", self._ble_buffer)
            
                # Clear buffer for next packet
                self._ble_buffer = ""

            

            #cd = int.from_bytes(data, "little", signed=False)
            # print(f"Data Received: {cd}")
            #self._update_ui(decoded_data)
            self._update_status("Reading ...")
        else:
            self._update_status("Not Reading ...")

    def characteristic_changed(self, handle, value):
        data = bytearray(value.tolist())
        self.emg_changed(data)

        #data=int.from_bytes(_value, "little", signed=False)
        # print(_value.decode('utf-8'),"-------",data)

    def connection_state_change(self, status, new_state):
        if new_state == BluetoothProfile.STATE_CONNECTED:
            print("conncted")
            show_toast("Connected!")
            self._update_status("Reading ...")
            if status == BluetoothGatt.GATT_SUCCESS:
                print("GATT SUCESS!! ")
                if self.bluetoothGatt:
                    self.bluetoothGatt.discoverServices()
                else:
                    show_toast("bluetoothGatt is None")
            # self.bluetoothGatt.requestMtu(32)
            # self.bluetoothGatt.getService(TARGET_SERVICE_UUID)

        elif new_state == BluetoothProfile.STATE_DISCONNECTED:
            show_toast("Disconnected!")
            self._update_status("Not Reading ...")
            return

    def scan_call(self, result):
        print("Python  ", result)
        device = result.getDevice()
        print(device.getName())
        if device.getAddress() == DEVICE_MAC:
            print('Device Found ')
            show_toast("Device Found!")
            self.bluetoothLeScanner.stopScan(self.psc)
            print('Device Found Stopping Scanning')
            show_toast("Stop Scanning")
            self.connectToDevice(context, device)
        else:
            pass
            #show_toast("Device Not Found!")

    def connect_ble(self):

        self.disconnect_ble()
        self.bluetoothAdapter = BluetoothAdapter.getDefaultAdapter()
        if not self.bluetoothAdapter.isEnabled():
            print("Bluetooth is Not Enable")
            enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            mActivity.startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT)
        else:
            print("Bluetooth is Already Enable")
        if self.bluetoothAdapter.isEnabled():
            self.bluetoothLeScanner = self.bluetoothAdapter.getBluetoothLeScanner()
            print(self.bluetoothLeScanner)
            self.pscan = PScanCallback(self.scan_call)
            print("pscan = ", self.pscan)
            self.psc = PythonScanCallback(self.pscan)
            print(self.psc)
            # start scanning
            self.bluetoothLeScanner.startScan(self.psc)
            show_toast("Start Scanning!")

    def disconnect_ble(self):
        if self.bluetoothGatt:
            self.bluetoothGatt.disconnect()
            self.bluetoothGatt.close()
            del self.bluetoothGatt
            del self.bluetoothLeScanner
            del self.pscan
            del self.psc
            del self.pbci
            del self.bgc


class MyApp(App):

    def build(self):

        if platform == 'android':
            self.get_runtime_permissions()
        self.title = "BLE App"
        return MainScreen()

    def get_runtime_permissions(self):
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            if all([res for res in results]):
                print("callback. All permissions granted.")
                show_toast("All permissions granted.")
            else:
                print("callback. Some permissions refused.")
                show_toast("Some permissions refused.")
            return True
        request_permissions([Permission.BLUETOOTH_CONNECT,
                             Permission.BLUETOOTH_SCAN, Permission.BLUETOOTH,
                             Permission.BLUETOOTH_ADMIN, Permission.ACCESS_FINE_LOCATION], callback)


if __name__ == '__main__':
    MyApp().run()
