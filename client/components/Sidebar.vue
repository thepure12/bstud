<template>
    <b-sidebar id="menu" header-class="bg-dark d-flex" bg-variant="dark" text-variant="white" backdrop-variant="dark"
        body-class="pb-2" width="360px" backdrop>
        <template #header>
            <b-row class="flex-nowrap flex-grow-1">
                <div><strong>Options</strong></div>
                <b-btn-close text-variant="white" v-b-toggle:menu></b-btn-close>
            </b-row>
        </template>
        <b-row class="gap-1 mt-1 mb-2">
            <BuyMeCoffee></BuyMeCoffee>
            <b-btn to="/feedback" class="flex-grow-1" variant="primary">Give Feedback</b-btn>
        </b-row>
        <b-card bg-variant="dark" header-class="bg-secondary h5">
            <template #header>
                Text Options
            </template>
            <b-form>
                <b-form-checkbox :checked="textOptions['include-passage-references']" @input="onReferencesInput" size="lg"
                    button-variant="secondary">References</b-form-checkbox>
                <b-form-checkbox :checked="textOptions['include-footnotes']" @input="onFootnotesInput"
                    size="lg">Footnotes</b-form-checkbox>
                <b-form-group :label="`Font Size: ${fontSize}`" label-size="lg">
                    <b-form-input :value="fontSize" type="range" min="7" max="24" @update="setFontSize" debounce="1000"
                        :disabled="trimming"></b-form-input>
                </b-form-group>
                <b-form-group :label="`Line Spacing: ${lineSpacing}`" label-size="lg">
                    <b-form-input :value="lineSpacing" type="range" :min="lhMin" max="3" step=".1" @update="setLineSpacing"
                        debounce="1000" :disabled="trimming"></b-form-input>
                </b-form-group>
                <b-form-radio-group :checked="textOptions.version" :options="versions" class="w-100"
                    button-variant="primary" buttons @change="onVersionChange"></b-form-radio-group>
            </b-form>
        </b-card>
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
        <b-card bg-variant="dark" header-class="bg-secondary h5">
            <template #header>
                Applications
                <b-link
                    href="https://www.knowableword.com/2013/04/12/how-to-study-the-bible/#:~:text=commentaries-,Application"
                    target="_blank">
                    <b-icon icon="info-circle" class="ml-2" variant="white" scale=1></b-icon>
                </b-link>
            </template>
            <b-form>
                <template v-for="(v, k) in applications">
                    <b-form-group :label="`${k}: ${v}`" label-size="lg">
                        <b-form-input :value="v" type="range" min="0" max="5" step="1"
                            @update="v => setApplication({ application: k, value: v })"></b-form-input>
                    </b-form-group>
                </template>
            </b-form>
        </b-card>
    </b-sidebar>
</template>
<script>
import { mapMutations, mapState } from 'vuex'
import { BIcon, BIconInfoCircle } from 'bootstrap-vue'
export default {
    components: {
        BIcon,
        BIconInfoCircle
    },
    data() {
        return {
            versions: ["ESV", "CSB", "NIV", "KJV", "NKJV"]
        }
    },
    computed: {
        ...mapState(["textOptions", "observations", "questions", "applications", "fontSize", "lineSpacing", "trimming"]),
        lhMin() {
            return .1
        },
        lhMax() {

        }
    },
    methods: {
        ...mapMutations(["setTextOption", "setObservation", "setQuestion", "setApplication", "setFontSize", "setLineSpacing"]),
        onReferencesInput(v) {
            this.setTextOption({ option: 'include-passage-references', value: v })
            this.$store.dispatch("fetchText")
        },
        onFootnotesInput(v) {
            this.setTextOption({ option: 'include-footnotes', value: v })
            this.$store.dispatch("fetchText")

        },
        onVersionChange(v) {
            this.setTextOption({ option: 'version', value: v })
            this.$store.dispatch("fetchText")
        }
    }
}
</script>