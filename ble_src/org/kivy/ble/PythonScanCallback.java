package org.kivy.ble;

import java.util.List;
import org.kivy.ble.CallbackWrapper;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.util.Log;
public final class PythonScanCallback extends ScanCallback{
    
    private CallbackWrapper callback;

    public PythonScanCallback(CallbackWrapper pythonCallback)
    {
        callback = pythonCallback;
    }

    @Override
    public void onBatchScanResults(List<ScanResult> results)
    {
        for (ScanResult result : results) {
            callback.onScanResult(result);
        }
    }

    @Override
    public void onScanFailed(int errorCode)
    {
        callback.onScanFailed(errorCode);
    }

    @Override
    public void onScanResult(int callbackType, ScanResult result)
    {
        callback.onScanResult(result);
    }
}
