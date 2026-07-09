package org.kivy.ble;
import android.bluetooth.le.ScanResult;

public interface CallbackWrapper{
        public void onScanFailed(int code);
        public void onScanResult(ScanResult result);
    }