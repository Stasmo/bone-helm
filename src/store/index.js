import Vue from 'vue'
import Vuex from 'vuex'

import bluetooth from './bluetooth'

Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
        count: 0,
        deviceReady: false,
        brightness: 0,
        color: null
    },
    mutations: {
        deviceReady(state) {
            state.deviceReady = true
        },
        setAnimation(state, animation) {
            state.animation = animation
        },
        setBrightness(state, brightness) {
            state.brightness = brightness
        },
        setColor(state, color) {
            state.color.rgba = {
                r: color[0],
                g: color[1],
                b: color[2],
                a: 1,
            }
        }
    },
    actions: {
        onDeviceReady({commit}) {
            commit('deviceReady', true)
        },
        onNewDetails({commit}, details) {
            console.log('new details', details)
            commit('setAnimation', details.animation)
            commit('setBrightness', details.brightness * 100)
            commit('setColor', details.color)
        }
    },
    modules: {
        bluetooth
    }
})

export default store