<template>
    <b-card bg-variant="dark" header-class="bg-secondary h5">
        <template #header>
            Interpretive Questions
            <b-link
                href="https://www.knowableword.com/2013/04/12/how-to-study-the-bible/#:~:text=observation-,Interpretation"
                target="_blank">
                <b-icon icon="info-circle" class="ml-2" variant="white" scale=1></b-icon>
            </b-link>
        </template>
        <b-form>
            <template v-for="(v, k) in questions">
                <b-form-group :label="`${k}: ${v}`" label-size="lg">
                    <b-form-input :value="v" type="range" min="0" max="5" step="1"
                        @update="v => setQuestion({ question: k, value: v })"></b-form-input>
                </b-form-group>
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
            "questions"
        ])
    },
    methods: {
        ...mapMutations([
            "setQuestion"
        ]),
    }
}
</script>