package org.kivy.ble;

import java.net.ConnectException;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CancellationException;
import java.util.concurrent.ExecutionException;
import java.util.HashMap;
import java.util.UUID;

import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.bluetooth.BluetoothProfile;
import org.kivy.ble.BluetoothGattCallBackWrapper;


public final class PythonBluetoothGattCallback extends BluetoothGattCallback
{
    
    private BluetoothGattCallBackWrapper callback;

    public PythonBluetoothGattCallback(BluetoothGattCallBackWrapper pythonCallback)
    {
        callback = pythonCallback;
    }

    @Override
    public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState)
    {
        callback.onConnectionStateChange(status, newState);
    }

    @Override
    public void onMtuChanged(BluetoothGatt gatt, int mtu, int status)
    {
        callback.onMtuChanged(mtu, status);
    }

    @Override
    public void onServicesDiscovered(BluetoothGatt gatt, int status)
    {
        callback.onServicesDiscovered(status);
    }

    @Override
    public void onCharacteristicRead(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status)
    {
        callback.onCharacteristicRead(characteristic.getInstanceId(), status, characteristic.getValue());
    }

    @Override
    public void onCharacteristicWrite(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status)
    {
        callback.onCharacteristicWrite(characteristic.getInstanceId(), status);
    }

    @Override
    public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic)
    {
        callback.onCharacteristicChanged(characteristic.getInstanceId(), characteristic.getValue());
    }

    @Override
    public void onDescriptorRead(BluetoothGatt gatt, BluetoothGattDescriptor descriptor, int status)
    {
        callback.onDescriptorRead(descriptor.getUuid().toString(), status, descriptor.getValue());
    }

    @Override
    public void onDescriptorWrite(BluetoothGatt gatt, BluetoothGattDescriptor descriptor, int status)
    {
        callback.onDescriptorWrite(descriptor.getUuid().toString(), status);
    }
}
