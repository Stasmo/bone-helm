<template>
    <v-container>
        <v-row>
            <v-col>
                <v-card>
                    <v-card-title>Animation and color control</v-card-title>
                    <v-card-text>
                        <v-row v-if="connectedDevice">
                            <v-col>
                                <v-slider
                                    label="brightness"
                                    @change="selectBrightness"
                                    v-model="brightness"
                                ></v-slider>
                                <v-select
                                    label="Select Animation"
                                    :items="animations"
                                    @change="selectAnimation"
                                    v-model="animation"
                                ></v-select>
                                <v-color-picker
                                    class="ma-2"
                                    hide-canvas
                                    show-swatches
                                    @update:color="selectColor"
                                ></v-color-picker>
                            </v-col>
                        </v-row>
                        <devices v-else></devices>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import bluetooth from '@/lib/bluetooth'
import DevicesComponent from '@/components/DevicesComponent'

export default {
    created() {
        console.log('Home page loaded')
        window.addEventListener('beforeunload', this.disconnect)
    },
    components: {
        'devices': DevicesComponent
    },
    computed: {
        ...mapState({
            connectedDevice: state => state.bluetooth.connectedDevice,
        }),
        ...mapState([
            'animation',
            'brightness',
            'color',
        ])
    },
    data: () => ({
        devices: [],
        animations: [
            'breath',
            'blink',
            'sparkle',
            'sparkle_pulse',
            'wave',
            'magma',
            'rainbow_sparkle',
            'rainbow',
        ].sort(),
        updateColorTimeout: null,
    }),
    methods: {
        ...mapActions([
            'sendMessage',
            'disconnect'
        ]),
        selectAnimation(v) {
            this.sendMessage({ type: bluetooth.MESSAGE_TYPES.UPDATE_ANIMATION, message: v })
        },
        selectBrightness(v) {
            console.log('b', v)
            this.sendMessage({ type: bluetooth.MESSAGE_TYPES.UPDATE_BRIGHTNESS, message: parseInt(v)/100 })
        },
        selectColor(v) {
            console.log('c', v)
            clearTimeout(this.updateColorTimeout)
            this.updateColorTimeout = setTimeout(() => this.sendMessage({ type: bluetooth.MESSAGE_TYPES.UPDATE_COLOR, message: `${v.rgba.r},${v.rgba.g},${v.rgba.b}` }), 200)
        }
    }
}
</script>