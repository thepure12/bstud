<template>
    <div>
        <b-row class="mb-3 py-2 gap-4 justify-content-center sticky-top bg-dark text-white h5">
            <!-- Text Reference -->
            <b-row class="my-auto gap-2">
                <div to="/">
                    <b-link class="text-white" to="/">
                        <font-awesome-icon icon="fa-solid fa-arrow-left" />
                    </b-link>
                </div>
                <div>{{ q }}</div>
            </b-row>
            <b-row class="border-right"></b-row>
            <!-- Tools -->
            <b-row class="tools my-auto gap-2">
                <template v-for="tool in tools">
                    <div :key="tool.name" :id="`tool-${tool.name}`" class="tool"
                        :class="activeTool === tool ? 'active' : ''" :style="`color: ${tool.color};`" tabindex="-1"
                        @click="onToolSelected(tool)">
                        <font-awesome-icon :icon="tool.icon" fixed-width />
                        <b-popover v-if="activeTool === tool" :target="`tool-${tool.name}`" placement="bottom"
                            triggers="click blur">
                            <template v-if="tool.name !== 'eraser'">
                                <verte :id="`${tool.name}-picker`" display="widget" :value="tool.color"
                                    @input="onColorChange">
                                </verte>
                            </template>
                            <b-form-input type="range" :value="tool.width" @input="onThicknessChange" min="1" max="50"
                                step="1"></b-form-input>
                            <div v-if="tool.name !== 'keyboard'"
                                :style="`border-bottom: ${tool.width}px solid ${tool.color}`"></div>
                            <div v-else :style="`font-size: ${tool.width}px; color: ${tool.color};`">Aa</div>
                        </b-popover>
                    </div>
                </template>
            </b-row>
            <b-row class="border-right"></b-row>
            <!-- Saved Colors -->
            <b-row class="gap-2 my-auto">
                <div v-for="(color, i) in savedColors" :key="`saved-color-${i}`">
                    <b-icon :id="`saved-color-${i}`" icon="circle-fill" scale="1.2" :style="`color: ${color};`"
                        @click="onSavedColor(color)"></b-icon>
                    <b-popover v-if="isActiveColor(color)" :target="`saved-color-${i}`" placement="bottom"
                        triggers="click blur" @shown="savingColor = true" @hide="savingColor = false">
                        <verte id="saved-color-picker" display="widget" :value="color"
                            @input="c => onSaveColorChange(i, c)">
                        </verte>
                    </b-popover>
                </div>
            </b-row>
            <b-row class="border-right"></b-row>
            <!-- Controls -->
            <b-row class="gap-4 my-auto">
                <div class="editor-control">
                    <font-awesome-icon icon="fa-solid fa-reply" @click="onUndo" />
                </div>
                <div class="editor-control">
                    <font-awesome-icon icon="fa-solid fa-reply" flip="horizontal" @click="onRedo" />
                </div>
                <div class="editor-control" @click="onToggleFullscreen">
                    <font-awesome-icon v-if="!isFullscreen" icon="fa-solid fa-up-right-and-down-left-from-center" />
                    <font-awesome-icon v-else icon="fa-solid fa-down-left-and-up-right-to-center" />
                </div>
                <div class="editor-control" @click="onSave">
                    <font-awesome-icon icon="fa-solid fa-floppy-disk" />
                </div>
                <div v-if="savedSheets && Object.keys(savedSheets).length" class="editor-control">
                    <font-awesome-icon v-b-toggle.savedSheets icon="fa-solid fa-folder-open" />
                    <b-sidebar id="savedSheets" title="Saved Sheets" header-class="bg-primary d-flex" bg-variant="dark"
                        text-variant="white" backdrop-variant="dark" body-class="py-2 px-4" width="360px" backdrop right>
                        <b-row v-for="(sheet, uuid) in savedSheets" :key="uuid" class="border-bottom border-primary py-2">
                            <b-link class="text-white" :to="`/editor?uuid=${uuid}`" @click="onLoadSaved">
                                <font-awesome-icon icon="fa-solid fa-file" class="mr-2" />
                                {{ sheet.textOptions.q }}
                            </b-link>
                            <font-awesome-icon :id="`trash-${uuid}`" icon="fa-solid fa-trash" class="ml-auto my-auto" />
                            <b-popover :target="`trash-${uuid}`" triggers="click blur" placement="left">
                                <b-btn variant="danger" @click="onDeleteSaved(uuid)">Delete</b-btn>
                            </b-popover>
                        </b-row>
                    </b-sidebar>
                </div>
                <div class="editor-control" @click="onDownload">
                    <font-awesome-icon icon="fa-solid fa-download" />
                </div>
            </b-row>
            <b-row class="border-right"></b-row>
            <!-- Disclaimer -->
            <b-row class="gap-2 my-auto">
                <div>Notes Beta</div>
                <div>
                    <font-awesome-icon id="beta-info" icon="fa-solid fa-circle-info" />
                    <b-popover target="beta-info" placement="bottom" triggers="click blur">
                        This editor is still a work in progress. There may be bugs. Please report them.
                    </b-popover>
                </div>
            </b-row>
        </b-row>
        <Sheets ref="sheets" :textContainers.sync="textContainers" :drawing="true" :brushColor="brushColor"
            :brushWidth="brushWidth" :erasing="erasing" :typing="typing" @objectAdded="onObjectAdded"
            @objectErased="onObjectErased">
        </Sheets>
    </div>
</template>
<script>
import Verte from 'verte';
import 'verte/dist/verte.css';
import { mapMutations } from 'vuex'
import {
    BIcon,
    BIconCircleFill,
} from 'bootstrap-vue'
export default {
    components: {
        Verte,
        BIcon,
        BIconCircleFill,
    },
    data() {
        return {
            tools: [
                {
                    name: "keyboard",
                    icon: "fa-solid fa-keyboard",
                    color: "#000000",
                    width: 14
                },
                {
                    name: "pencil",
                    icon: "fa-solid fa-pencil",
                    color: "#000000",
                    width: 1
                },
                {
                    name: "highligher",
                    icon: "fa-solid fa-highlighter",
                    color: "hsla(63,76%,62%,0.68)",
                    width: 13
                },
                {
                    name: "eraser",
                    icon: "fa-solid fa-eraser",
                    color: "lightgrey",
                    width: 10
                }
            ],
            activeTool: null,
            erasing: false,
            typing: false,
            brushColor: "#000000",
            savedColors: ["hsl(207,44%,49%)", "hsl(248,53%,57%)", "hsl(10,100%,60%)"],
            brushWidth: 1,
            h: [],
            isFullscreen: false,
            lockHistory: false,
            undoHistory: [],
            redoHistory: [],
            textContainers: [],
            savedSheets: null
        }
    },
    computed: {
        q() {
            return this.$store.state.textOptions.q
        },
        uuid() {
            return this.$route.query.uuid || this.uuidv4()
        }
    },
    methods: {
        ...mapMutations([
            "setDownloading",
            "setPrintable",
            "setPassages",
            "setObservation",
            "setTextOption",
            "setFontSize",
            "setLineSpacing",
            "setQuestion",
            "setApplication",
        ]),
        onSetBrush(brush) {

        },
        async onToolSelected(tool) {
            if (tool.name === "eraser") {
                this.erasing = true
                await this.$nextTick()
            } else if (this.erasing) {
                this.erasing = false
                await this.$nextTick()
            }
            if (tool.name === "keyboard") {
                this.typing = true
            } else if (this.typing) {
                this.typing = false
                await this.$nextTick()
            }
            this.activeTool = tool
            this.onColorChange(tool.color)
            this.onThicknessChange(tool.width)
        },
        onEraserSelected() {

        },
        onSavedColor(color) {
            let savedColor = new Color(color)
            let toolAlpha = new Color(this.activeTool.color).alpha || 1
            // savedColor.alpha = toolAlpha
            let hsla = `hsla(${Math.round(savedColor.hsl.h)}`
            hsla += `,${Math.round(savedColor.hsl.s)}%`
            hsla += `,${Math.round(savedColor.hsl.l)}%`
            hsla += `,${toolAlpha})`
            this.onColorChange(hsla)
        },
        isActiveColor(color) {
            return new Color(this.brushColor).toString({ format: "hsl" }) == new Color(color).toString({ format: "hsl" })
        },
        onSaveColorChange(i, color) {
            this.savedColors[i] = color
            this.onColorChange(color)
        },
        onColorChange(color) {
            this.brushColor = color
            this.activeTool.color = color
        },
        onThicknessChange(thickness) {
            thickness = parseInt(thickness)
            this.brushWidth = thickness
            this.activeTool.width = thickness
        },
        onObjectAdded(canvas) {
            if (this.lockHistory) return
            this.undoHistory.push([canvas, JSON.stringify(canvas)])
        },
        onObjectErased(canvas) {
            if (this.lockHistory) return
            this.undoHistory.push([canvas, JSON.stringify(canvas)])
        },
        onUndo() {
            if (this.undoHistory.length > 0) {
                this.lockHistory = true
                let [canvas, content] = this.undoHistory.pop()
                this.redoHistory.push([canvas, content])
                if (this.undoHistory.length >= 1 && canvas._objects.length > 1) {
                    [canvas, content] = this.undoHistory[this.undoHistory.length - 1]
                    canvas.loadFromJSON(content, () => {
                        canvas.renderAll()
                        this.lockHistory = false
                    })
                } else {
                    canvas.clear()
                    canvas.renderAll()
                    this.lockHistory = false
                }
            }
        },
        onRedo() {
            if (this.redoHistory.length > 0) {
                this.lockHistory = true
                let [canvas, content] = this.redoHistory.pop()
                this.undoHistory.push([canvas, content])
                canvas.loadFromJSON(content, () => {
                    canvas.renderAll()
                    this.lockHistory = false
                })
            }
        },
        onTrash() {
            // this.$root.$emit('bv::hide::popover', 'trash')
            // this.canvas._objects.forEach(o => this.h.push(o))
            // this.canvas.clear()
        },
        onErase() {
            this.canvas.freeDrawingBrush = new fabric.EraserBrush(canvas)
        },
        onToggleFullscreen() {
            if (this.isFullscreen)
                document.exitFullscreen()
            else
                document.body.requestFullscreen()
            this.isFullscreen = !this.isFullscreen
        },
        onSave() {
            const data = {
                canvases: this.$refs.sheets.$refs.canvases.map(ref => ref.canvas),
                textOptions: this.$store.state.textOptions,
                passages: this.$store.state.passages,
                observations: this.$store.state.observations,
                questions: this.$store.state.questions,
                applications: this.$store.state.applications,
                fontSize: this.$store.state.fontSize,
                lineSpacing: this.$store.state.lineSpacing,
            }
            this.savedSheets[this.uuid] = data
            localStorage.setItem("savedSheets", JSON.stringify(this.savedSheets))
            this.savedSheets = JSON.parse(localStorage.getItem("savedSheets"))
            this.$bvToast.toast(`Worksheet Saved`, {
                title: 'Success',
                autoHideDelay: 100,
                variant: "success"
            })
        },
        onLoadSaved() {
            this.loadSaved()
        },
        onDeleteSaved(uuid) {
            delete this.savedSheets[uuid]
            this.savedSheets = JSON.parse(JSON.stringify(this.savedSheets))
            localStorage.setItem("savedSheets", JSON.stringify(this.savedSheets))
            this.$nextTick(
                this.$bvToast.toast(`Worksheet Deleted`, {
                    title: 'Success',
                    autoHideDelay: 100,
                    variant: "success"
                })
            )
        },
        onDownload() {
            this.setDownloading(true)
            this.setPrintable(true)
            this.$nextTick(() => {
                let opt = {
                    margin: .25,
                    filename: this.q,
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
        },
        uuidv4() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
                .replace(/[xy]/g, function (c) {
                    const r = Math.random() * 16 | 0,
                        v = c == 'x' ? r : (r & 0x3 | 0x8);
                    return v.toString(16);
                });
        },
        loadSaved() {
            if (this.uuid) {
                let savedSheets = this.savedSheets
                if (savedSheets) {
                    let sheet = savedSheets[this.uuid]
                    if (sheet) {
                        // Text Options
                        for (const [key, val] of Object.entries(sheet.textOptions)) {
                            this.setTextOption({ option: key, value: val })
                        }
                        // Observations
                        for (const [key, val] of Object.entries(sheet.observations)) {
                            this.setObservation({ observation: key, value: val })
                        }
                        // Questions
                        for (const [key, val] of Object.entries(sheet.questions)) {
                            this.setTextOption({ question: key, value: val })
                        }
                        // Applications
                        for (const [key, val] of Object.entries(sheet.applications)) {
                            this.setTextOption({ application: key, value: val })
                        }
                        // Passages
                        this.setPassages(sheet.passages)
                        // Font Size
                        this.setFontSize(sheet.fontSize)
                        // Line Spacing
                        this.setLineSpacing(sheet.lineSpacing)
                        this.$nextTick(() => {
                            this.$refs.sheets.$refs.canvases.forEach((ref, i) => {
                                ref.canvas.loadFromJSON(JSON.stringify(sheet.canvases[i]), () => {
                                    ref.canvas.renderAll()
                                })
                            })
                        })
                    }
                }
            }
        }
    },
    created() {
        this.onToolSelected(this.tools[1])
        this.savedSheets = JSON.parse(localStorage.getItem("savedSheets")) || {}
    },
    mounted() {
        
        this.loadSaved()
    }
}
</script>