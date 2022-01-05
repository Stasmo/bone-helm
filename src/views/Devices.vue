<template>
    <v-container>
        <v-row>
            <v-col>
                <v-card v-if="connectedDevice" class="mb-2">
                    <v-card-title>{{ connectedDevice.name }}</v-card-title>
                    <v-card-subtitle>Connected device</v-card-subtitle>
                    <v-card-text>
                        <v-simple-table>
                            <tr>
                                <td>Name</td>
                                <td>{{ connectedDevice.name }}</td>
                            </tr>
                            <tr>
                                <td>ID</td>
                                <td>{{ connectedDevice.id }}</td>
                            </tr>
                        </v-simple-table>
                        <v-form @submit="sendMessage({ type: bluetooth.MESSAGE_TYPES.DEBUG_MESSAGE, message: message }); message = ''">
                            <v-text-field
                                placeholder="Send message to device"
                                v-model="message"
                            ></v-text-field>
                        </v-form>
                        
                        <div class="text-right">
                            <v-btn @click="sendMessage({ type: bluetooth.MESSAGE_TYPES.DEBUG_MESSAGE, message: message }); message = ''" class="mb-2">Send</v-btn> 
                        </div>
                        
                        <br>
                        <v-btn @click="disconnect">Disconnect</v-btn>
                    </v-card-text>
                </v-card>
                <v-card>
                    <v-card-title>
                        Devices
                        <v-spacer></v-spacer>
                        <v-btn
                            @click="scanForPeripherals"
                            :disabled="scanning || !deviceReady"
                            :loading="scanning"
                            color="primary"
                        >
                            Scan
                        </v-btn>
                    </v-card-title>
                    <v-card-text>
                        <v-row>
                            <v-col>
                                <v-list>
                                    <v-list-item v-if="scanning && !devices.length">
                                        <v-list-item-content>
                                            Scanning
                                        </v-list-item-content>
                                    </v-list-item>
                                    <v-list-item dense v-for="device in devices" :key="device.id">
                                        <v-list-item-content>
                                            <v-list-item-title class="pa-2" style="line-height: 2.5rem">
                                                {{ device.name || device.id }}
                                                <v-btn
                                                    v-if="!connectedDevice"
                                                    :elevation="2"
                                                    class="float-right"
                                                    icon
                                                    color="primary"
                                                    dark
                                                    @click="connect(device.id)"
                                                >
                                                    <v-icon>mdi-bluetooth-connect</v-icon>
                                                </v-btn>
                                            </v-list-item-title>
                                            <!-- <div v-if="device.data" >
                                                <div v-for="(data, serviceName) in device.data" :key="serviceName">
                                                    <div v-if="data['2a00']">
                                                        Name: {{ decode(data['2a00']) }}
                                                    </div>
                                                    <div v-if="data['2a19']">
                                                        Battery level: {{ buf2dec(data['2a19']) }}
                                                    </div>
                                                </div>
                                            </div> -->
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-list>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import bluetooth from '@/lib/bluetooth'

function buf2dec(buffer) { // buffer is an ArrayBuffer
  return [...new Uint8Array(buffer)].map(x => x.toString(10).padStart(2, '0')).join('');
}

export default {
    computed: {
        ...mapState(['deviceReady']),
        ...mapState({
            devices: state => state.bluetooth.devices,
            scanning: state => state.bluetooth.scanning,
            connectedDevice: state => state.bluetooth.connectedDevice,
            connectedDeviceId: state => state.bluetooth.connectedDeviceId,
        })
    },
    created() {
        console.log('Devices page loaded')
        if (this.deviceReady) {
            this.init()
        }
        window.addEventListener('beforeunload', this.disconnect)
    },
    destroyed() {
        clearInterval(this.autoscanInterval)
    },
    data: () => ({
        connections: [],
        disableScanButton: false,
        autoscanInterval: null,
        message: '',
        bluetooth,
    }),
    watch: {
        deviceReady(val) {
            if (val){
                this.init()
            }
        },
        connectedDeviceId(val) {
            if (!val) {
                this.scanForPeripherals()
            } else {
                this.$router.push('Home')
            }
        }
    },
    methods: {
        ...mapActions([
            'scanForPeripherals',
            'connect',
            'disconnect',
            'sendMessage'
        ]),
        init() {
            window.ble.enable(
                () => {
                    console.log('Bluetooth is enabled.')
                    this.scanForPeripherals()
                    this.autoscanInterval = setInterval(this.scanForPeripherals, 40000)
                },
                () => {
                    console.error('Bluetooth failed to load.')
                }
            );
        },
        buf2dec,
        disableScan(timeoutSeconds) {
            this.disableScanButton = true
            setTimeout(() =>{ this.disableScanButton = false }, (timeoutSeconds || 5) * 1000)
        },
    }
}
</script>