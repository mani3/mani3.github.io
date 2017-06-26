title: CBCentralManagerのQueueを指定してみる
Date: 2017-06-24 01:16:02
Modified: 2017-06-24 01:16:02
Category: development
Tags: ios
Slug: ios-cbcentralmanager
Summary: CoreBluetooth の CBCentralManager の Queue を設定した場合とnilの場合とで検証してみた

iOSでBluetoothデバイスを利用するアプリを開発したときに、 `CBCentralManagerDelegate` 内で Realm の書き込みを行ったら `RLMException` が起きたので、この際にデリゲートが呼び出されたときのスレッドがどうなっているのか調べてみた。  

### CBCentralManagerのイニシャライザ

```swift
/// https://developer.apple.com/documentation/corebluetooth/cbcentralmanager/1518695-init
convenience init(delegate: CBCentralManagerDelegate?, queue: DispatchQueue?)
```

この引数の `queue` に以下の3種類を指定して実行してみたときの、 Delegateで呼び出されるスレッドがどうなっているか試してみた。

- Main Dispatch Queue (nilを指定)
- Serial
- Concurrent 


### 試したコード

```swift
import UIKit
import CoreBluetooth

class ViewController: UIViewController {

    let serial = DispatchQueue(label: "serial")
    let concurrent = DispatchQueue(label: "concurrent", attributes: .concurrent)
    
    var manager: CBCentralManager?

    @IBAction func mainQueue(_ sender: UIButton) {
        if manager != nil {
            manager?.stopScan()
            manager = nil
        }
        manager = CBCentralManager(delegate: self, queue: nil)
        NSLog("%@, %@", #function, Thread.current.description)
    }
    
    @IBAction func serialQueue(_ sender: UIButton) {
        if manager != nil {
            manager?.stopScan()
            manager = nil
        }
        manager = CBCentralManager(delegate: self, queue: serial)
        NSLog("%@, %@", #function, Thread.current.description)
    }
    
    @IBAction func concurrentQueue(_ sender: UIButton) {
        if manager != nil {
            manager?.stopScan()
            manager = nil
        }
        manager = CBCentralManager(delegate: self, queue: concurrent)
        NSLog("%@, %@", #function, Thread.current.description)
    }
}

extension ViewController: CBCentralManagerDelegate {
    
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        NSLog("%@, %@", #function, Thread.current.description)
        guard central.state == .poweredOn else { return }
        central.scanForPeripherals(withServices: nil, options: nil)
    }
    
    /// ペリフェラルが検出されたら呼ばれる
    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
        NSLog("%@, %@", #function, Thread.current.description)
    }
}
```

### Main Dispatch Queue (queue = nil の場合)

メインスレッドで実行した場合、 ペリフェラルの検出（`centralManager(_:didDiscover:advertisementData:rssi:)`）は必ずメインスレッドで呼び出された。

```
CentralManager[478:416991] mainQueue, <NSThread: 0x17406e840>{number = 1, name = main}
CentralManager[478:416991] centralManagerDidUpdateState, <NSThread: 0x17406e840>{number = 1, name = main}
CentralManager[478:416991] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x17406e840>{number = 1, name = main}
CentralManager[478:416991] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x17406e840>{number = 1, name = main}
CentralManager[478:416991] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x17406e840>{number = 1, name = main}
CentralManager[478:416991] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x17406e840>{number = 1, name = main}
```

### Serial を指定した場合

シリアルの `DispatchQueue` を指定した場合、同一のスレッドで呼び出されると思ったが、検出されたペリフェラルによって別スレッドで呼び出されていた。

```
CentralManager[478:416991] serialQueue, <NSThread: 0x17406e840>{number = 1, name = main}
CentralManager[478:417123] [CoreBluetooth] XPC connection invalid
CentralManager[478:417123] centralManagerDidUpdateState, <NSThread: 0x174075300>{number = 3, name = (null)}
CentralManager[478:417062] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x17407a500>{number = 4, name = (null)}
CentralManager[478:417123] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x174075300>{number = 3, name = (null)}
CentralManager[478:417062] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x17407a500>{number = 4, name = (null)}
CentralManager[478:417123] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x174075300>{number = 3, name = (null)}
```

### Concurrent を指定した場合

Concurrentな `DispatchQueue` を指定した場合は、予想通り別スレッドで呼び出されていた。
```
CentralManager[478:416991] concurrentQueue, <NSThread: 0x17406e840>{number = 1, name = main}
CentralManager[478:417143] [CoreBluetooth] XPC connection invalid
CentralManager[478:417143] centralManagerDidUpdateState, <NSThread: 0x17407a500>{number = 5, name = (null)}
CentralManager[478:417122] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x17407b380>{number = 6, name = (null)}
CentralManager[478:417143] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x17407a500>{number = 5, name = (null)}
CentralManager[478:417122] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x17407b380>{number = 6, name = (null)}
CentralManager[478:417122] centralManager(_:didDiscover:advertisementData:rssi:), <NSThread: 0x17407b380>{number = 6, name = (null)}
```

### まとめ

メインスレッドの場合以外は、 `CBCentralManagerDelegate` は別スレッドで呼び出されるようなので気を付けたい。

