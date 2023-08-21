<template>
    <b-col class="d-flex flex-column">
        <template v-for="(v, k) in applications">
            <b-card v-if="v" class="flex-grow-1" header-class="h6 px-2 py-1" body-class="col d-flex flex-column">
                <template #header>{{ k }}</template>
                <b-row v-for="i in v" class="flex-grow-1" :key="`${k}-${i}`">
                    <b-card class="flex-grow-1" body-class="px-2 py-1">Application</b-card>
                </b-row>
            </b-card>
        </template>
    </b-col>
</template>
<script>
import { mapState } from "vuex"
export default {
    computed: {
        ...mapState(["applications"])
    }
}
</script>