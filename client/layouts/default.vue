<template>
    <div class="d-flex flex-column vh-100">
        <Header v-if="!printable"></Header>
        <div :class="!printable ? 'scrolltainer' : ''">
            <div :class="!printable ? 'app-container' : 'printable'">
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
        ...mapState(["printable", "textOptions", "downloading"])
    },
    watch: {
        printable(val) {
            if (val) this.$nextTick(() => this.doPrint())
        }
    },
    methods: {
        ...mapMutations(["setTextOption", "setObservation", "setPrintable"]),
        doPrint() {
            if (!this.downloading) {
                this.$nextTick(() => print())
                this.setPrintable(false)
            }
        }
    },
    created() {
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
        this.$store.dispatch("fetchText")
            .then(() => {
                this.setPrintable(query.print === "true")
            })
    }
}
</script>
<style scoped>
@media print {
    @page {
        size: landscape;
    }
}

.scrolltainer {
    /* display: flex; */
    flex-grow: 1;
    overflow-x: auto;
}

.app-container {
    display: flex;
    margin: 1rem;
    margin-inline: max(calc((100% - 11in) / 2), 1rem);
    padding: 1rem;
    border: 1px dashed steelblue;
    width: 11in;
    height: 8.5in;
}

.printable {
    display: flex;
    height: 100vh;
}

@media only screen and (max-width: 11in) {
    .app-container {
        max-width: calc(100vw - 2rem);
        height: unset;
        aspect-ratio: calc(8.5/11);
    }

    @media (orientation: portrait) {

        .app-container {
            margin-top: 2rem;
            position: relative;
        }

        .app-container::before {
            position: absolute;
            display: block;
            top: -1.75rem;
            left: 0;
            text-align: center;
            width: 100%;
            content: "Switch to landscape for better preview";
        }
    }

    @media (orientation: landscape) {
        .app-container {
            height: calc(100vh - 5.5rem);
        }
    }

}
</style>