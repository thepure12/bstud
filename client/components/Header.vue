<template>
    <b-navbar class="flex-wrap justify-content-start" type="dark" variant="primary" toggleable sticky>
        <b-form class="flex-grow-1" @submit.prevent="onSearch">
            <b-input-group>
                <b-form-input :value="textOptions.q" @input="onSearchInput" type="search"
                    placeholder="Search"></b-form-input>
                <template #prepend>
                    <b-btn v-b-toggle:menu>
                        <b-icon icon="gear"></b-icon>
                        Vathéos
                    </b-btn>
                </template>
                <template #append>
                    <b-btn type="submit">Search</b-btn>
                    <b-btn @click="onShare">
                        <b-icon icon="share"></b-icon>
                    </b-btn>
                </template>
            </b-input-group>
        </b-form>
        <Sidebar />
        <b-modal id="share-modal" title="Share" header-class="bg-primary text-white" body-class="d-flex flex-column gap-3"
            footer-class="bg-primary" ok-title="Close" ok-variant="secondary" ok-only centered>
            <img :src="qrURL" class="mx-auto" alt="">
            <b-input-group>
                <b-form-input :value="shortShare" disabled></b-form-input>
                <template #append>
                    <b-btn @click="onCopy" :variant="copyVariant">
                        <b-icon icon="clipboard"></b-icon>
                    </b-btn>
                </template>
            </b-input-group>
            <b-alert variant="success" fade :show="copied" @dismissed="copyVariant = 'secondary'"
                @dismiss-count-down="(v) => copied = v">
                Copied To Clipboard
            </b-alert>
        </b-modal>
    </b-navbar>
</template>
<script>
import { mapState } from 'vuex'
import { BIcon, BIconThreeDotsVertical, BIconGear, BIconShare, BIconClipboard } from "bootstrap-vue"
export default {
    components: {
        BIcon, BIconThreeDotsVertical, BIconGear, BIconShare, BIconClipboard
    },
    data() {
        return {
            search: "",
            copyVariant: "secondary",
            copied: false,
            shortShare: ""
        }
    },
    computed: {
        ...mapState(["textOptions", "observations", "questions", "applications", "fontSize", "lineSpacing"]),
        shareURL() {
            let src = "https://" + window.location.host.replace("www.", "") + `?search=${this.textOptions.q}`
            // let src = "https://vatheos.com" + `?search=${this.textOptions.q}`
            src += `&references=${this.textOptions["include-passage-references"]}`
            src += `&footnotes=${this.textOptions["include-footnotes"]}`
            src += `&fontSize=${this.fontSize}`
            src += `&lineSpacing=${this.lineSpacing}`
            // Observations
            src += "&observations="
            src += Object.keys(this.observations)
                .filter(x => this.observations[x])
                .map(x => x.split("/")[0].toLocaleLowerCase())
                .join(",")
            // Questions and Applications
            for (let settings of [this.questions, this.applications]) {
                for (let [setting, value] of Object.entries(settings)) {
                    if (value) {
                        let _setting = setting.split("/")[0].toLocaleLowerCase()
                        src += `&${_setting}=${value}`
                    }
                }
            }
            return encodeURI(src)
        },
        qrURL() {
            return "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=" + this.shareURL
        }
    },
    methods: {
        onSearchInput(v) {
            this.$store.commit("setTextOption", { option: "q", value: v })
        },
        onSearch() {
            // this.$store.commit("setTextOption", { option: "q", value: this.search })
            this.$store.dispatch("fetchText")
        },
        onShare() {
            this.$axios.post(`/share`, { url: this.shareURL })
                .then((res) => {
                    this.shortShare = res.data.link || this.shareURL
                    this.$nextTick()
                    this.$bvModal.show("share-modal")
                })
            // this.$bvModal.show("share-modal")
        },
        onCopy() {
            this.copyVariant = "secondary"
            setTimeout(() => {
                navigator.clipboard.writeText(this.shortShare)
                    .then(() => {
                        this.copyVariant = "success"
                        this.copied = 2
                    }, () => this.copyVariant = "danger")
            }, 200)

        }
    },
}
</script>
<style scoped>
.navbar {
    gap: 1rem;
}
</style>