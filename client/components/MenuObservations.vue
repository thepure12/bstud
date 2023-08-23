<template>
    <b-card bg-variant="dark" header-class="bg-secondary h5">
        <template #header>
            Observations
            <b-link href="https://www.knowableword.com/2013/04/12/how-to-study-the-bible/#:~:text=Bible-,Observation"
                target="_blank">
                <b-icon icon="info-circle" class="ml-2" variant="white" scale=1></b-icon>
            </b-link>
        </template>
        <b-form>
            <template v-for="(v, k) in observations">
                <b-form-checkbox :checked="v" @input="v => setObservation({ observation: k, value: v })" size="lg">
                    {{ k }}
                </b-form-checkbox>

            </template>
        </b-form>
    </b-card>
</template>
<script>
import { mapState, mapMutations } from 'vuex'
import { BIcon, BIconInfoCircle } from 'bootstrap-vue'
export default {
    components: {
        BIcon,
        BIconInfoCircle
    },
    computed: {
        ...mapState([
            "observations"
        ])
    },
    methods: {
        ...mapMutations([
            "setObservation"
        ]),
    }
}
</script>