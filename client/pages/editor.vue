<template>
    <div>
        <b-row class="mb-3 py-2 justify-content-around sticky-top bg-dark text-white h5">
            <b-row class="my-auto gap-2">
                <div to="/">
                    <b-link class="text-white" to="/">
                        <font-awesome-icon icon="fa-solid fa-arrow-left" />
                    </b-link>
                </div>
                <div>{{ q }}</div>
            </b-row>
            <b-row class="tools my-auto gap-2">
                <template v-for="tool in tools">
                    <div :key="tool.name" :id="`tool-${tool.name}`" class="tool"
                        :class="activeTool === tool ? 'active' : ''" :style="`color: ${tool.color};`" tabindex="-1"
                        @click="onToolSelected(tool)">
                        <!-- <b-icon :icon="tool.icon" :style="`color: ${tool.color};`">
                    </b-icon> -->
                        <font-awesome-icon :icon="tool.icon" />
                        <b-popover v-if="activeTool === tool" :target="`tool-${tool.name}`" placement="bottom"
                            triggers="click blur">
                            <template v-if="tool.name !== 'eraser'">
                                <verte :id="`${tool.name}-picker`" display="widget" :value="tool.color"
                                    @input="onColorChange">
                                </verte>
                            </template>
                            <b-form-input type="range" :value="tool.width" @input="onThicknessChange" min="1" max="50"
                                step="1"></b-form-input>
                            <div :style="`border-bottom: ${tool.width}px solid ${tool.color}`"></div>
                        </b-popover>
                    </div>
                </template>
                <!-- <div class="tool" :class="erasing ? 'active' : ''" @click="onEraserSelected">
                    <font-awesome-icon id="eraser" icon="fa-solid fa-eraser" />
                    <b-popover v-if="erasing" target="eraser" placement="bottom" triggers="click blur">
                        <b-form-input type="range" :value="tool.width" @input="onThicknessChange" min="1" max="50"
                            step="1"></b-form-input>
                        <div :style="`border-bottom: ${tool.width}px solid gray;`"></div>
                    </b-popover>
                </div> -->
            </b-row>
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
            <b-row class="gap-2 my-auto">
                <div>Editor Beta</div>
                <div>
                    <font-awesome-icon id="beta-info" icon="fa-solid fa-circle-info" />
                    <b-popover target="beta-info" placement="bottom" triggers="click blur">
                        This editor is still a work in progress. There may be bugs. Please report them.
                    </b-popover>
                </div>
            </b-row>
            <b-row class="gap-3 my-auto">
                <div class="editor-control">
                    <font-awesome-icon icon="fa-solid fa-reply" @click="onUndo" />
                </div>
                <div class="editor-control">
                    <font-awesome-icon icon="fa-solid fa-reply" flip="horizontal" @click="onRedo" />
                </div>
                <!-- <b-btn id="trash">
                    <b-icon icon="trash"></b-icon>
                </b-btn>
                <b-popover target="trash" triggers="click blur" placement="bottom">
                    <b-btn @click="onTrash">Erase All</b-btn>
                </b-popover> -->
                <div class="editor-control" @click="onToggleFullscreen">
                    <font-awesome-icon v-if="!isFullscreen" icon="fa-solid fa-expand" />
                    <font-awesome-icon v-else icon="fa-solid fa-compress" />
                </div>
            </b-row>
        </b-row>
        <Sheets :textContainers.sync="textContainers" :drawing="true" :brushColor="brushColor" :brushWidth="brushWidth"
            :erasing="erasing" @objectAdded="onObjectAdded">
        </Sheets>
    </div>
</template>
<script>
import Verte from 'verte';
import 'verte/dist/verte.css';
import {
    BIcon,
    BIconArrow90degLeft,
    BIconArrow90degRight,
    BIconTrash,
    BIconFullscreen,
    BIconFullscreenExit,
    BIconArrowLeft,
    BIconCircleFill,
    BIconEraser,
    BIconPencilFill,
    BIconTelephoneMinus
} from 'bootstrap-vue'
export default {
    components: {
        Verte,
        BIcon,
        BIconArrow90degLeft,
        BIconArrow90degRight,
        BIconTrash,
        BIconFullscreen,
        BIconFullscreenExit,
        BIconArrowLeft,
        BIconCircleFill,
        BIconEraser,
        BIconPencilFill
    },
    data() {
        return {
            tools: [
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
            brushColor: "#000000",
            savedColors: ["hsl(207,44%,49%)", "hsl(248,53%,57%)", "hsl(10,100%,60%)"],
            brushWidth: 1,
            h: [],
            isRedoing: false,
            isFullscreen: false,
            addedHistory: [], //History of which canvas was last added to
            textContainers: [],

        }
    },
    computed: {
        q() {
            return this.$store.state.textOptions.q
        }
    },
    methods: {
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
            this.addedHistory.push(canvas)
        },
        onUndo() {
            if (this.addedHistory.length > 0) {
                const canvas = this.addedHistory.pop()
                this.h.push([canvas, canvas._objects.pop()])
                canvas.renderAll()
            }
        },
        onRedo() {
            if (this.h.length > 0) {
                this.isRedoing = true;
                const [canvas, object] = this.h.pop()
                canvas.add(object)
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
        }
    },
    created() {
        this.onToolSelected(this.tools[0])
    },
    mounted() {
    }
}
</script>