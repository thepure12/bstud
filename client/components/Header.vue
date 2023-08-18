<template>
    <b-navbar class="flex-wrap justify-content-start" type="dark" variant="primary" toggleable sticky>
        <b-navbar-toggle target="menu" class="border-white"></b-navbar-toggle>
        <b-navbar-brand>
            Vathéos
        </b-navbar-brand>
        <b-form class="flex-grow-1" @submit.prevent="onSearch">
            <b-input-group class="search-group">
                <b-form-input v-model="search" type="search" placeholder="Search"></b-form-input>
                <template #prepend>
                    <b-btn class="print" @click="$store.commit('setPrintable', true)">Print</b-btn>
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
export default {
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