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
            </b-form>
        </b-card>
        <b-card bg-variant="dark" header-class="bg-secondary h5">
            <template #header>
                Observations
            </template>
            <b-form>
                <template v-for="(v, k) in observations">
                    <b-form-checkbox :checked="v" @input="v => setObservation({ observation: k, value: v })"
                        size="lg">
                        {{ k }}
                    </b-form-checkbox>
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
        ...mapState(["textOptions", "observations", "fontSize"])
    },
    methods: {
        ...mapMutations(["setTextOption", "setObservation", "setFontSize"]),
    }
}
</script>