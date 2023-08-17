<template>
  <b-col class="d-flex flex-column gap-1">
    <b-row class="gap-1 flex-grow-1" :class="printable ? 'printable-sheet' : 'sheet'">
      <b-col class="pr-2 h-100" :class="printable ? '' : 'overflow-auto'" :style="`line-height: ${lineSpacing}rem;`">
        <span class="pre-wrap" :style="`font-size: ${fontSize}pt;`">{{ text }}</span>
      </b-col>
      <b-col class="d-flex flex-column h-100" :style="downloading ? 'height: 765px !important;' : ''">
        <b-row class="flex-grow-1 gap-1 mr-1">
          <template v-for="(v, k) in observations">
            <b-card v-if="v" :key="k" class="flex-grow-1 observation" body-class="px-2 py-1">
              {{ k }}
            </b-card>
          </template>
        </b-row>
      </b-col>
      <div v-if="text && !printable" class="fixed-bottom p-2 pr-4">
        <b-btn class="float-right" @click="onDownload">Download</b-btn>
      </div>
    </b-row>
    <b-row v-if="totalQuestions" class="gap-1" :class="printable ? 'printable-sheet' : 'sheet'">
      <b-col class="d-flex flex-column gap-1 mr-1">
        <template v-for="(v, k) in questions">
          <b-card v-if="v" class="flex-grow-1" header-class="h6" body-class="col d-flex flex-column">
            <template #header>{{ k }}</template>
            <b-row v-for="i in v" class="flex-grow-1" :key="`${k}-${v}`">
              <b-card class="flex-grow-1" body-class="px-2 py-1">Question</b-card>
              <b-card class="flex-grow-1" body-class="px-2 py-1">Answer</b-card>
            </b-row>
          </b-card>
        </template>
      </b-col>
    </b-row>
  </b-col>
</template>
<script>
import { mapState, mapMutations } from "vuex"

export default {
  data() {
    return {
    }
  },
  computed: {
    ...mapState(["textOptions", "observations", "questions", "passages", "fontSize", "printable", "downloading", "lineSpacing"]),
    text() {
      return this.passages.join("\n\n")
        .replace(/\n +/gm, "\n")
        .replace(/ {2,}/gm, " ")
        .replace(/\n{2,}/gm, "\n")
        .trim()
    },
    totalQuestions() {
      return Object.values(this.questions).reduce((a, b) => a + b, 0)
    },
    downloadUrl() {
      return `http://localhost:8000/text?${new URLSearchParams(this.textOptions)}&font-size=${this.fontSize}&download`
    }
  },
  methods: {
    ...mapMutations(["setDownloading", "setPrintable"]),
    onDownload() {
      let element = document.querySelector("body")
      let windowHeight = element.querySelector(".col").scrollHeight
      this.setDownloading(true)
      this.setPrintable(true)
      this.$nextTick(() => {
        console.log(windowHeight);
        let opt = {
          margin: .25,
          filename: this.textOptions.q,
          jsPDF: { unit: "in", format: "letter", orientation: "landscape" },
          html2canvas: { windowHeight: windowHeight }
        }
        html2pdf().from(element).set(opt).save().then(() => {
          this.setDownloading(false)
          this.setPrintable(false)
        })
      })
    }
  },
}
</script>
<style scoped>
.card-body {
  font-size: 10pt;
  font-weight: bold;
}

.new-sheet {
  border-top: 1px dashed steelblue;
}
</style>