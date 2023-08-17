<template>
  <b-col id="sheets" class="d-flex flex-column gap-1">
    <b-row class="gap-1 flex-grow-1" :class="printable ? 'printable-sheet' : 'sheet'">
      <b-col ref="text-container" class="pr-2 h-100" :class="printable ? '' : 'overflow-auto'"
        :style="`line-height: ${lineSpacing}rem;`">
        <span class="pre-wrap" :style="`font-size: ${fontSize}pt;`">{{ sheet1Text }}</span>
      </b-col>
      <b-col class="d-flex flex-column h-100" >
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
    <div v-if="downloading && (totalQuestions || sheet2Text)" class="mb-2 p-2"></div>
    <b-row v-if="totalQuestions || sheet2Text" class="gap-1" :class="printable ? 'printable-sheet' : 'sheet'">
      <b-col class="d-flex flex-column gap-1 mr-1">
        <span v-if="sheet2Text" class="pre-wrap" :style="`font-size: ${fontSize}pt;`">{{ sheet2Text }}</span>
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
      sheet1Text: "",
      sheet2Text: "",
      textContainer: null
    }
  },
  computed: {
    ...mapState(["textOptions", "observations", "questions", "passages", "fontSize", "printable", "downloading", "lineSpacing"]),
    text() {
      let text = this.passages.join("\n\n")
        .replace(/\n +/gm, "\n")
        .replace(/ {2,}/gm, " ")
        .replace(/\n{2,}/gm, "\n")
        .trim()
      return text
    },
    totalQuestions() {
      return Object.values(this.questions).reduce((a, b) => a + b, 0)
    },
    downloadUrl() {
      return `http://localhost:8000/text?${new URLSearchParams(this.textOptions)}&font-size=${this.fontSize}&download`
    }
  },
  watch: {
    text() {
      this.trimText()
    },
    fontSize() {
      this.trimText()
    },
    lineSpacing() {
      this.trimText()
    }
  },
  methods: {
    ...mapMutations(["setDownloading", "setPrintable"]),
    async trimText() {
      this.sheet1Text = this.text
      this.sheet2Text = ""
      await this.$nextTick()
      while (this.textContainer.scrollHeight - this.textContainer.clientHeight > 0) {
        let last_sentence = this.sheet1Text.lastIndexOf(".", this.sheet1Text.lastIndexOf(".") - 1) + 1;
        this.sheet1Text = this.sheet1Text.substring(0, last_sentence);
        this.sheet2Text = this.text.substring(last_sentence).trim()
        await this.$nextTick()
      }
    },
    onDownload() {
      this.setDownloading(true)
      this.setPrintable(true)
      this.$nextTick(() => {
        let element = document.querySelector("#sheets")
        let windowHeight = element.clientHeight
        if (this.sheet2Text === "") windowHeight += 100
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
  mounted() {
    this.textContainer = this.$refs["text-container"]
  }
}
</script>
<style scoped>
.card-body {
  font-size: 10pt;
  font-weight: bold;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.new-sheet {
  border-top: 1px dashed steelblue;
}
</style>