<template>
  <b-row class="gap-1 flex-grow-1">
    <b-col class="pr-2">
      <span class="pre-wrap" :style="`font-size: ${fontSize}pt;`">{{ text }}</span>
    </b-col>
    <b-col class="d-flex flex-column h-100">
      <b-row class="flex-grow-1 gap-1 mr-1">
        <b-col v-for="(col, i) in observations" class="px-0 d-flex flex-column gap-1" :key="`col-${i}`">
          <template v-for="(v, k) in col">
            <b-card v-if="v" :key="k" class="flex-grow-1" body-class="px-2 py-1">
              {{ k }}
            </b-card>
          </template>

        </b-col>
      </b-row>
    </b-col>
    <div v-if="text && !printable" class="fixed-bottom p-2">
      <b-btn class="float-right" :href="downloadUrl" target="_blank">Download</b-btn>
    </div>
  </b-row>
</template>
<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      printable: false,
      showOptions: false,
    }
  },
  computed: {
    ...mapState(["textOptions", "observations", "passages", "fontSize"]),
    text() {
      return this.passages.join("\n\n")
        .replace(/\n +/gm, "\n")
        .replace(/ {2,}/gm, " ")
        .replace(/\n{2,}/gm, "\n")
        .trim()
    },
    downloadUrl() {
      return `http://localhost:8000/text?${new URLSearchParams(this.textOptions)}&font-size=${this.fontSize}&download`
    }
  },
  methods: {
  },
}
</script>
<style scoped>
.card-body {
  font-size: 10pt;
  font-weight: bold;
}
</style>