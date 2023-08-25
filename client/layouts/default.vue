<template>
    <div id="app" class="d-flex flex-column vh-100">
        <Header v-if="!printable && showHeader"></Header>
        <div :class="!printable ? 'scrolltainer' : ''">
            <div>
                <Nuxt />
            </div>
        </div>
    </div>
</template>
<script>
import { mapState, mapMutations } from 'vuex'

export default {
    data() {
        return {
            // showHeader: true
        }
    },
    computed: {
        ...mapState([
            "printable",
            "downloading",
            "observations",
            "questions",
            "applications",
            "fontSize",
            "lineSpacing"
        ]),
        showHeader() {
            return this.$route.name != "editor"
        }
    },
    watch: {
        printable(val) {
            if (val) this.$nextTick(() => this.doPrint())
        }
    },
    methods: {
        ...mapMutations([
            "setTextOption",
            "setObservation",
            "setQuestion",
            "setApplication",
            "setPrintable",
            "setFontSize",
            "setLineSpacing"
        ]),
        doPrint() {
            if (!this.downloading) {
                this.$nextTick(() => print())
            }
        }
    },
    created() {
        screen.orientation.lock("landscape").catch(() => { })
        onafterprint = () => this.setPrintable(false)
        // this.$nuxt.$on('hideHeader', () => {
        //     this.showHeader = false
        // })
        // this.$nuxt.$on('showHeader', () => {
        //     this.showHeader = true
        // })
        let query = this.$route.query

        // Text options
        if (query.search)
            this.setTextOption({ option: "q", value: query.search })
        if (query.references)
            this.setTextOption({ option: "include-passage-references", value: query.references === "true" })
        if (query.footnotes)
            this.setTextOption({ option: "include-footnotes", value: query.footnotes === "true" })
        if (query.fontSize)
            this.setFontSize(parseInt(query.fontSize) || this.fontSize)
        if (query.lineSpacing)
            this.setLineSpacing(parseFloat(query.lineSpacing) || this.lineSpacing)
        if (query.version) {
            this.setTextOption({ option: "version", value: query.version })
        }

        // Observations
        if (query.observations) {
            const _observations = query.observations.split(",")
            for (const setting in this.observations) {
                let _setting = setting.split("/")[0].toLocaleLowerCase()
                this.setObservation({ observation: setting, value: _observations.includes(_setting) })
            }
        }

        // Questions and Applications
        for (const settings of [
            { setting: this.questions, mutation: this.setQuestion, name: "question" },
            { setting: this.applications, mutation: this.setApplication, name: "application" }
        ]) {
            for (const setting in settings.setting) {
                let _setting = setting.split("/")[0].toLocaleLowerCase()
                // console.log(_setting);
                if (query[_setting]) {
                    let value = parseInt(query[_setting]) || query[_setting] === "true"
                    console.log(settings)
                    settings.mutation({ [settings.name]: setting, value: value })
                }
            }
        }

        this.$store.dispatch("fetchText")
            .then(() => {
                this.setPrintable(query.print === "true")
            })
    },
}
</script>
<style scoped></style>