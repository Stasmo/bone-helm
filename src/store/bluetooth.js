// import bluetooth from '@/lib/bluetooth'

let ble = null;
let scanStopTimeout = null;
let completeMessage = ""
const bluefruit = {
    serviceUUID: "6e400001-b5a3-f393-e0a9-e50e24dcca9e",
    txCharacteristic: "6e400002-b5a3-f393-e0a9-e50e24dcca9e",
    rxCharacteristic: "6e400003-b5a3-f393-e0a9-e50e24dcca9e"
}

function stringToBytes(string) {
    var array = new Uint8Array(string.length);
    for (var i = 0, l = string.length; i < l; i++) {
        array[i] = string.charCodeAt(i);
    }
    return array.buffer;
}

function bytesToString(buffer) {
    return String.fromCharCode.apply(null, new Uint8Array(buffer));
}

let module = {
    state: {
        scanning: false,
        devices: [],
        connectedDevice: null,
    },
    mutations: {
        setScanning(state, scanning) {
            state.scanning = scanning
        },
        setConnectedDevice(state, device) {
            console.log('Setting connected device', {device})
            state.connectedDevice = device
        },
        setDevices(state, devices) {
            state.devices = devices
        }
    },
    actions: {
        scanForPeripherals({ commit, state }) {
            if (!ble) return console.error('Scan called before device ready')
            if (state.connectedDevice) return console.log('Not scanning while connected to a device')
            console.log('Starting scan')
            commit('setScanning', true)
            if (scanStopTimeout) {
                ble.stopScan()
                clearTimeout(scanStopTimeout)
            }
            scanStopTimeout = setTimeout(() => { commit('setScanning', false) }, 30000)
            ble.scan([], 30, device => {

                let exists = state.devices.find(d => d.id == device.id)
                if (exists) { 
                    state.devices[state.devices.indexOf[exists]] = { ...exists, ...device }
                } else {
                    state.devices.push(device)
                }

                ble.isConnected(device.id, () => commit('setConnectedDevice', device))

                state.devices.sort((a,b) => a.id > b.id ? 1 : -1)
            }, failure => {
                console.error('Scan failure', failure)
                commit('setScanning', false)
            })
        },
        stopScanning({ commit }) {
            console.log('Stopping scan')
            commit('setScanning', false)
            ble.stopScan()
            clearTimeout(scanStopTimeout)
        },
        onConnect({ commit, dispatch }, device) {
            commit('setConnectedDevice', device);
            dispatch('stopScanning')
            console.log(device)
            let encodedMessage = stringToBytes("s:")
            for(let c of device.characteristics) {
                // if (c.properties.includes('Read')) {
                //     ble.read(
                //         device.id,
                //         c.service,
                //         c.characteristic,
                //         message => dispatch('onRecieveMessage', "read" + message),
                //         error => console.error('error reading', error)
                //     )
                // }
                if (c.properties.includes('Notify')) {
                    ble.startNotification(
                        device.id,
                        c.service,
                        c.characteristic,
                        message => dispatch('onRecieveMessage', message),
                        console.error
                    )
                }
            }
            ble.write(
                device.id,
                bluefruit.serviceUUID,
                bluefruit.txCharacteristic,
                encodedMessage,
                console.log,
                console.error,
            )
            // ble.startNotification(
            //     device.id,
            //     bluefruit.seviceUUID,
            //     bluefruit.rxCharacteristic,
            //     message => dispatch('onRecieveMessage', message),
            //     console.error
            // )
            // ble.read(
            //     device.id,
            //     bluefruit.seviceUUID,
            //     bluefruit.rxCharacteristic,
            //     message => dispatch('onRecieveMessage', message),
            //     error => console.error('error reading', error)
            // )
        },
        connect({ state, dispatch }, deviceId) {
            if (state.connectedDevice) {
                dispatch('disconnect')
            }
            ble.connect(deviceId,
                device => dispatch('onConnect', device),
                failure => dispatch('onDisconnect', failure)
            )
        },
        onDisconnect({ state, commit }, failure) {
            console.error(failure)
            if (state.connectedDevice) {
                commit('setConnectedDevice', null)
            }
        },
        disconnect({ state, commit }) {
            console.log('disconnect called')
            if (state.connectedDevice) {
                console.log('disconnect device')
                ble.disconnect(state.connectedDevice.id, () => commit('setConnectedDevice', null))
            }
        },
        onDeviceReady({ dispatch }) {
            ble = window.ble;
            ble.autoConnect('E0:CC:80:4C:C1:CF', device => dispatch('onConnect', device))
        },
        sendMessage({ state }, { type, message }) {
            if (state.connectedDevice) {
                let encodedMessage = stringToBytes(type + message)
                console.log('Sending message', {encodedMessage})
                ble.write(
                    state.connectedDevice.id,
                    bluefruit.serviceUUID,
                    bluefruit.txCharacteristic,
                    encodedMessage,
                    console.log,
                    console.error,
                )
            } else {
                console.error('Cannot send message, no connected device.')
            }
        },
        onRecieveMessage({dispatch}, message) {
            completeMessage += bytesToString(message)
            try {
                let parsedMessage = JSON.parse(completeMessage)
                if (parsedMessage.type == "details") {
                    completeMessage = ""
                    dispatch('onNewDetails', parsedMessage)
                }
            } catch(e) {
                console.log('Not complete', completeMessage)
                // message incomplete
            }
        }
    },
}

export default module