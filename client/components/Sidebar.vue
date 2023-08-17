<template>
    <b-sidebar title="Options" id="menu" header-class="bg-dark" bg-variant="dark" text-variant="white"
        backdrop-variant="dark" backdrop>
        <b-card bg-variant="dark" header-class="bg-secondary h5">
            <template #header>
                Text Options
            </template>
            <b-form>
                <b-form-checkbox :checked="textOptions['include-passage-references']"
                    @input="v => setTextOption({ option: 'include-passage-references', value: v })" size="lg"
                    button-variant="secondary">References</b-form-checkbox>
                <b-form-checkbox :checked="textOptions['include-footnotes']"
                    @input="v => setTextOption({ option: 'include-footnotes', value: v })"
                    size="lg">Footnotes</b-form-checkbox>
                <b-form-group :label="`Font Size: ${fontSize}`" label-size="lg">
                    <b-form-input :value="fontSize" type="range" min="7" max="24" @update="setFontSize"></b-form-input>
                </b-form-group>
                <b-form-group :label="`Line Spacing: ${lineSpacing}`" label-size="lg">
                    <b-form-input :value="lineSpacing" type="range" :min="lhMin" max="2" step=".1"
                        @update="setLineSpacing"></b-form-input>
                </b-form-group>
            </b-form>
        </b-card>
        <b-card bg-variant="dark" header-class="bg-secondary h5">
            <template #header>
                Observations
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
            <template #header>Questions</template>
            <b-form>
                <template v-for="(v, k) in questions">
                    <b-form-group :label="`${k}: ${v}`" label-size="lg">
                        <b-form-input :value="v" type="range" min="0" max="5" step="1"
                            @update="v => setQuestion({ question: k, value: v })"></b-form-input>
                    </b-form-group>
                </template>
            </b-form>
        </b-card>
    </b-sidebar>
</template>
<script>
import { mapMutations, mapState } from 'vuex'
export default {
    data() {
        return {}
    },
    computed: {
        ...mapState(["textOptions", "observations", "questions", "fontSize", "lineSpacing"]),
        lhMin() {
            return .1
        },
        lhMax() {

        }
    },
    methods: {
        ...mapMutations(["setTextOption", "setObservation", "setQuestion", "setFontSize", "setLineSpacing"]),
    }
}
</script>