<template>
    <div id="app" class="d-flex flex-column vh-100">
        <Header v-if="!printable"></Header>
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
            showHeader: true
        }
    },
    computed: {
        ...mapState([
            "printable",
            "downloading",
            "observations",
            "questions",
            "applications"
        ])
    },
    watch: {
        printable(val) {
            if (val) this.$nextTick(() => this.doPrint())
        }
    },
    methods: {
        ...mapMutations(["setTextOption", "setObservation", "setQuestion", "setApplication", "setPrintable"]),
        doPrint() {
            if (!this.downloading) {
                this.$nextTick(() => print())
            }
        }
    },
    created() {
        screen.orientation.lock("landscape").catch(() => { })
        onafterprint = () => this.setPrintable(false)
        this.$nuxt.$on('hideHeader', () => {
            this.showHeader = false
        })
        this.$nuxt.$on('showHeader', () => {
            this.showHeader = true
        })
        let query = this.$route.query
        if (query.search)
            this.setTextOption({ option: "q", value: query.search })
        if (query.references)
            this.setTextOption({ option: "include-passage-references", value: query.references === "true" })
        if (query.footnotes)
            this.setTextOption({ option: "include-footnotes", value: query.footnotes === "true" })

        for (const settings of [
            { setting: this.observations, mutation: this.setObservation, name: "observation" },
            { setting: this.questions, mutation: this.setQuestion, name: "question" },
            { setting: this.applications, mutation: this.setApplication, name: "application" }
        ]) {
            for (const setting in settings.setting) {
                let _setting = setting.split("/")[0].toLocaleLowerCase()
                console.log(_setting);
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