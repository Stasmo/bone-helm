import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
// import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);

export default new Vuetify({
    theme: {
        themes: {
            light: {
                // primary: colors.deepPurple,
                // secondary: colors.purple.lighten2,
                // accent: '#8c9eff',
                // error: '#b71c1c',
            }
        }
    }
});
