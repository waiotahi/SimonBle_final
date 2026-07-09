package org.kivy.ble;


public interface BluetoothGattCallBackWrapper
    {
        public void onConnectionStateChange(int status, int newState);
        public void onMtuChanged(int mtu, int status);
        public void onServicesDiscovered(int status);
        public void onCharacteristicChanged(int handle, byte[] value);
        public void onCharacteristicRead(int handle, int status, byte[] value);
        public void onCharacteristicWrite(int handle, int status);
        public void onDescriptorRead(String uuid, int status, byte[] value);
        public void onDescriptorWrite(String uuid, int status);
    }