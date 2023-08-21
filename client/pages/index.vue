<template>
  <div>
    <b-col id="sheets" class="d-flex flex-column gap-1">
      <template v-for="(text, k) in sheetTexts">
        <b-row v-if="isSheetVisible(text, k)" :id="k" class="flex-grow-1 gap-1 overflow-auto" :key="k" :ref="`textContainer`"
          :class="printable ? 'printable-sheet' : 'sheet'">
          <b-col v-if="text || k === 'sheet1'" class="overflow-auto mr-2">
            <span class="pre-wrap" :style="`font-size: ${fontSize}pt; line-height: ${lineSpacing}rem;`">{{ text }}</span>
          </b-col>
          <!-- Observations -->
          <Observations v-if="k === 'sheet1'"></Observations>
          <!-- Questions -->
          <Questions v-if="k === 'sheet2' && totalQuestions"></Questions>
          <!-- Applications -->
          <Applications v-if="k === 'sheet2' && !text && totalApplications"></Applications>
          <Applications v-if="k === 'sheet3' && totalApplications"></Applications>
        </b-row>
        <div v-if="downloading" class="mb-2 p-2"></div>
      </template>

    </b-col>
    <div v-if="text && !printable" class="fixed-bottom d-flex justify-content-end gap-1 p-2 pr-4">
      <b-btn class="btn-rotate" @click="rotateDevice">
        <b-iconstack>
          <b-icon stacked icon="phone" scale="0.6"></b-icon>
          <b-icon stacked icon="arrow-clockwise" scale="1.5"></b-icon>
        </b-iconstack>

      </b-btn>
      <b-btn @click="onDownload">
        <b-icon icon="download" animation="cylon-vertical"></b-icon>
      </b-btn>
    </div>
  </div>
</template>
<script>
import { mapState, mapMutations } from "vuex"
import { BIcon, BIconDownload, BIconPhone, BIconstack, BIconArrowClockwise } from 'bootstrap-vue'

export default {
  components: {
    BIcon,
    BIconstack,
    BIconDownload,
    BIconPhone,
    BIconArrowClockwise
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
    ...mapState([
      "textOptions",
      "observations",
      "questions",
      "applications",
      "passages",
      "fontSize",
      "printable",
      "downloading",
      "lineSpacing",
      "trimming"
    ]),
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
    totalApplications() {
      return Object.values(this.applications).reduce((a, b) => a + b, 0)
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
    totalQuestions(oldVal, newVal) {
      if (oldVal === 0 || newVal == 0)
        this.trimText(1)
    },
    totalApplications(oldVal, newVal) {
      if (oldVal === 0 || newVal == 0)
        this.trimText(1)
    }
  },
  methods: {
    ...mapMutations(["setDownloading", "setPrintable", "setTrimming"]),
    async trimText(sheet) {
      if (sheet === 1 && this.trimming) return
      this.setTrimming(true)
      if (sheet === 1) {
        this.resetSheetText()
        this.sheetTexts[`sheet${sheet}`] = this.text
      }
      await this.$nextTick()
      while (
        this.textContainers[sheet - 1].scrollHeight - this.textContainers[sheet - 1].clientHeight > 0
      ) {
        let lastSentenctIndex = this.sheetTexts[`sheet${sheet}`].lastIndexOf(".", this.sheetTexts[`sheet${sheet}`].lastIndexOf(".") - 1) + 1;
        if (lastSentenctIndex === 0) break
        let lastSentence = this.sheetTexts[`sheet${sheet}`].substring(lastSentenctIndex).trim()
        this.sheetTexts[`sheet${sheet + 1}`] = `${lastSentence} ${this.sheetTexts[`sheet${sheet + 1}`] || ''}`
        this.sheetTexts[`sheet${sheet}`] = this.sheetTexts[`sheet${sheet}`].substring(0, lastSentenctIndex);
        await this.$nextTick()
      }
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
    isSheetVisible(text, sheet) {
      switch (sheet) {
        case "sheet1":
          return true
        case "sheet2":
          return text != "" || this.totalQuestions > 0 || this.totalApplications > 0
        case "sheet3":
          if (text) {
            return true
          } else {
            return this.sheetTexts.sheet2 != "" && this.totalQuestions > 0 && this.totalApplications > 0
          }
        default:
          return text != ""
      }
    },
    rotateDevice() {
      if (screen.orientation.type === "landscape-primary") {
        document.exitFullscreen()
      } else {
        document.exitFullscreen()
        document.body.requestFullscreen()
          .then(() => screen.orientation.lock("landscape-primary")
            // .then(() => document.exitFullscreen())
            .catch())
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