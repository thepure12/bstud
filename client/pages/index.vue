<template>
  <div>
    <b-col id="sheets" class="d-flex flex-column gap-1">
      <template v-for="(text, k) in sheetTexts">
        <b-row v-if="text || k === 'sheet1'" :id="k" class="flex-grow-1 overflow-auto" :key="k" :ref="`textContainer`"
          :class="printable ? 'printable-sheet' : 'sheet'">
          <b-col class="overflow-auto mr-2">
            <span class="pre-wrap" :style="`font-size: ${fontSize}pt; line-height: ${lineSpacing}rem;`">{{ text }}</span>
          </b-col>
          <!-- Observations -->
          <b-col v-if="k === 'sheet1'" class="d-flex flex-column">
            <b-row class="flex-grow-1 gap-1 mr-1">
              <template v-for="(v, k) in observations">
                <b-card v-if="v" :key="k" class="flex-grow-1 observation" body-class="px-2 py-1">
                  {{ k }}
                </b-card>
              </template>
            </b-row>
          </b-col>
          <!-- Questions -->
          <b-col v-if="k === 'sheet2' && totalQuestions" class="d-flex flex-column">
            <template v-for="(v, k) in questions">
              <b-card v-if="v" class="flex-grow-1" header-class="h6 px-2 py-1" body-class="col d-flex flex-column">
                <template #header>{{ k }}</template>
                <b-row v-for="i in v" class="flex-grow-1" :key="`${k}-${v}`">
                  <b-card class="flex-grow-1" body-class="px-2 py-1">Question</b-card>
                  <b-card class="flex-grow-1" body-class="px-2 py-1">Answer</b-card>
                </b-row>
              </b-card>
            </template>
          </b-col>
        </b-row>
        <div v-if="downloading" class="mb-2 p-2"></div>
      </template>

    </b-col>
    <div v-if="text && !printable" class="fixed-bottom p-2 pr-4">
      <b-btn class="float-right" @click="onDownload">
        <b-icon icon="download" animation="cylon-vertical"></b-icon>
      </b-btn>
    </div>
  </div>
</template>
<script>
import { mapState, mapMutations } from "vuex"
import { BIcon, BIconDownload } from 'bootstrap-vue'

export default {
  components: {
    BIcon,
    BIconDownload
  },
  data() {
    return {
      sheetTexts: {
        sheet1: "",
        sheet2: "",
        sheet3: "",
        sheet4: "",
        sheet5: "",
        sheet6: "",
        sheet7: "",
        sheet8: "",
        sheet9: "",
        sheet10: "",
      },
      textContainers: [],
      numOfSheets: 1
    }
  },
  computed: {
    ...mapState(["textOptions", "observations", "questions", "passages", "fontSize", "printable", "downloading", "lineSpacing", "trimming"]),
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
      this.trimText(1)
    },
    fontSize() {
      this.trimText(1)
    },
    lineSpacing() {
      this.trimText(1)
    },
    totalQuestions() {
      this.trimText(1)
    }
  },
  methods: {
    ...mapMutations(["setDownloading", "setPrintable", "setTrimming"]),
    async trimText(sheet) {
      if (sheet === 1 && this.trimming) return
      this.setTrimming(true)
      // console.log("Sheet: " + sheet);
      if (sheet === 1) {
        this.resetSheetText()
        this.sheetTexts[`sheet${sheet}`] = this.text
      }
      await this.$nextTick()
      // console.log(this.textContainers[sheet - 1]);
      while (
        this.textContainers[sheet - 1].scrollHeight - this.textContainers[sheet - 1].clientHeight > 0
      ) {
        // console.log(`Scroll Diff: ${this.textContainers[sheet - 1].scrollHeight - this.textContainers[sheet - 1].clientHeight}`);
        let lastSentenctIndex = this.sheetTexts[`sheet${sheet}`].lastIndexOf(".", this.sheetTexts[`sheet${sheet}`].lastIndexOf(".") - 1) + 1;
        if (lastSentenctIndex === 0) break
        let lastSentence = this.sheetTexts[`sheet${sheet}`].substring(lastSentenctIndex).trim()
        // console.log("Last Sentence: " + lastSentence);
        this.sheetTexts[`sheet${sheet + 1}`] = `${lastSentence} ${this.sheetTexts[`sheet${sheet + 1}`] || ''}`
        this.sheetTexts[`sheet${sheet}`] = this.sheetTexts[`sheet${sheet}`].substring(0, lastSentenctIndex);
        // console.log("Trimmed Sheet Text: " + this.sheetTexts[`sheet${sheet}`]);
        await this.$nextTick()
      }
      // console.log(this.sheetTexts[`sheet${sheet + 1}`]);
      // console.log(Object.keys(this.sheetTexts).length)
      // console.log(this.textContainers)
      if (this.textContainers.length > sheet)
        this.trimText(sheet + 1)
      else
        this.setTrimming(false)
    },
    resetSheetText() {
      for (const [sheet, value] of Object.entries(this.sheetTexts)) {
        this.sheetTexts[sheet] = ""
      }
    },
    async scaleSheets() {
      await this.$nextTick()
      const scrollTainer = document.querySelector(".scrolltainer")
      const root = document.querySelector(":root")
      root.style.setProperty("--scale", 1)
      let scale = getComputedStyle(root).getPropertyValue("--scale")
      while (scrollTainer.scrollWidth > scrollTainer.clientWidth && scale > 0) {
        root.style.setProperty("--scale", parseFloat(scale) - .01)
        scale = getComputedStyle(root).getPropertyValue("--scale")
        await this.$nextTick()
      }
    },
    onDownload() {
      this.setDownloading(true)
      this.setPrintable(true)
      this.$nextTick(() => {
        // let element = document.querySelector("#sheets")
        let opt = {
          margin: .25,
          filename: this.textOptions.q,
          jsPDF: { unit: "in", format: "letter", orientation: "landscape" },
        }
        let worker = html2pdf().set(opt).from(this.textContainers[0])
        worker = worker.toPdf()
        this.textContainers.slice(1).forEach((element, i) => {
          worker = worker
            .get('pdf')
            .then(pdf => {
              pdf.addPage()
            })
            .from(element)
            .toContainer()
            .toCanvas()
            .toPdf()
        })
        worker.save().then(() => {
          this.setDownloading(false)
          this.setPrintable(false)
        })
      })
    }
  },
  created() {
    let portrait = window.matchMedia("(orientation: portrait)");
    let scaleSheets = this.scaleSheets

    portrait.addEventListener("change", function (e) {
      if (e.matches) {
        // Portrait mode
      } else {
        scaleSheets()
      }
    })
  },
  mounted() {
    this.textContainers = this.$refs["textContainer"]
    this.scaleSheets()
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