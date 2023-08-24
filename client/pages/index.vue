<template>
  <div>
    <Sheets :textContainers.sync="textContainers"></Sheets>
    <div v-if="passages && !printable" class="fixed-bottom d-flex justify-content-end gap-1 p-2 pr-4">
      <b-btn to="editor">
        <b-icon icon="pencil"></b-icon>
      </b-btn>
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
import { BIcon, BIconDownload, BIconPhone, BIconstack, BIconArrowClockwise, BIconPencil } from 'bootstrap-vue'

export default {
  components: {
    BIcon,
    BIconstack,
    BIconDownload,
    BIconPhone,
    BIconArrowClockwise,
    BIconPencil
  },
  data() {
    return {
      textContainers: []
    }
  },
  computed: {
    ...mapState([
      "textOptions",
      "passages",
      "printable",

    ]),
    downloadUrl() {
      return `http://localhost:8000/text?${new URLSearchParams(this.textOptions)}&font-size=${this.fontSize}&download`
    }
  },
  methods: {
    ...mapMutations(["setDownloading", "setPrintable"]),
    rotateDevice() {
      if (screen.orientation.type === "landscape-primary") {
        document.exitFullscreen()
      } else {
        document.exitFullscreen()
        document.body.requestFullscreen()
          .then(() => screen.orientation.lock("landscape-primary")
            .catch())
      }

    },
    onDownload() {
      this.setDownloading(true)
      this.setPrintable(true)
      this.$nextTick(() => {
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
  }
}
</script>