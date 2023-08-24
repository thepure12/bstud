<template>
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
                <b-form-input :value="lineSpacing" type="range" min=".1" max="3" step=".1" @update="setLineSpacing"
                    debounce="1000" :disabled="trimming"></b-form-input>
            </b-form-group>
            <b-form-radio-group :checked="textOptions.version" :options="versions" class="w-100" button-variant="primary"
                buttons @change="onVersionChange"></b-form-radio-group>
        </b-form>
    </b-card>
</template>
<script>
import { mapState, mapMutations } from 'vuex'
export default {
    computed: {
        ...mapState([
            "textOptions",
            "versions",
            "fontSize",
            "lineSpacing",
            "trimming"
        ])
    },
    methods: {
        ...mapMutations([
            "setTextOption",
            "setFontSize",
            "setLineSpacing"
        ]),
        onReferencesInput(v) {
            this.setTextOption({ option: 'include-passage-references', value: v })
            this.$store.dispatch("fetchText")
        },
        onFootnotesInput(v) {
            this.setTextOption({ option: 'include-footnotes', value: v })
            this.$store.dispatch("fetchText")
        },
        onVersionChange(v) {
            this.setTextOption({ option: "version", value: v })
            this.$store.dispatch("fetchText")

        }
    }
}
</script>