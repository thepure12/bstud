<template>
    <b-navbar class="flex-wrap justify-content-start" type="dark" variant="primary" toggleable sticky>
        <!-- <b-navbar-toggle target="menu" class="bg-secondary text-white py-2">
            <template #default="{ expanded }">
                <b-icon icon="gear"></b-icon>
                Vathéos
            </template>
        </b-navbar-toggle> -->
        <!-- <b-navbar-brand>
            Vathéos
        </b-navbar-brand> -->
        <b-form class="flex-grow-1" @submit.prevent="onSearch">
            <b-input-group>
                <b-form-input v-model="search" type="search" placeholder="Search"></b-form-input>
                <template #prepend>
                    <!-- <b-btn class="print" @click="$store.commit('setPrintable', true)">Print</b-btn> -->
                    <b-btn v-b-toggle:menu>
                        <b-icon icon="gear"></b-icon>
                        Vathéos
                    </b-btn>
                </template>
                <template #append>
                    <b-btn type="submit">Search</b-btn>
                </template>
            </b-input-group>
        </b-form>
        <Sidebar />
    </b-navbar>
</template>
<script>
import { BIcon, BIconThreeDotsVertical, BIconGear } from "bootstrap-vue"
export default {
    components: {
        BIcon, BIconThreeDotsVertical, BIconGear
    },
    data() {
        return {
            search: ""
        }
    },
    methods: {
        onSearch() {
            this.$store.commit("setTextOption", { option: "q", value: this.search })
            this.$store.dispatch("fetchText")
        }
    }
}
</script>
<style scoped>
.navbar {
    gap: 1rem;
}
</style>