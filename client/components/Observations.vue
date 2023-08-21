<template>
    <b-col class="d-flex flex-column">
        <b-row class="flex-grow-1 gap-1">
            <b-card class="w-100" body-class="px-2 py-1">Main Point</b-card>
            <template v-for="(v, k) in observations">
                <b-card v-if="v" :key="k" class="flex-grow-1 observation" body-class="px-2 py-1">
                    {{ k }}
                </b-card>
            </template>
        </b-row>
    </b-col>
</template>
<script>
import { mapState } from "vuex"
export default {
    computed: {
        ...mapState(["observations"])
    }
}

</script>