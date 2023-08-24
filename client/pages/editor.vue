<template>
    <div class="m-3 ">
        <b-row v-if="canvas" class="mb-3 justify-content-around"
            :style="`border-bottom: ${brushThickness}px solid ${brushColor}`">
            <b-form-group class="my-auto">
                <b-btn to="/">
                    <b-icon icon="arrow-left"></b-icon>
                </b-btn>
            </b-form-group>
            <b-form-group label="Color">
                <b-row class="gap-2">
                    <verte ref="verte" picker="square" :value="brushColor" @input="onColorChange"
                        :colorHistory.sync="brushColorHistory"></verte>
                    <b-row class="gap-2">
                        <div>
                            <b-icon icon="circle-fill" scale="1.2" :style="`color: ${brushColorHistory[0]};`"
                                @click="onColorChange(brushColorHistory[0])"></b-icon>
                        </div>
                        <div>
                            <b-icon icon="circle-fill" scale="1.2" :style="`color: ${brushColorHistory[1]};`"
                                @click="onColorChange(brushColorHistory[1])"></b-icon>
                        </div>
                        <div>
                            <b-icon icon="circle-fill" scale="1.2" :style="`color: ${brushColorHistory[2]};`"
                                @click="onColorChange(brushColorHistory[2])"></b-icon>
                        </div>
                    </b-row>

                </b-row>
            </b-form-group>
            <b-form-group label="Thickness">
                <b-form-input type="range" :value="canvas.freeDrawingBrush.width" @input="onThicknessChange" min="1"
                    max="50" step="1"></b-form-input>
            </b-form-group>
            <b-form-group class="my-auto">
                <b-row class="gap-1">
                    <b-btn @click="onUndo">
                        <b-icon icon="arrow90deg-left"></b-icon>
                    </b-btn>
                    <b-btn @click="onRedo">
                        <b-icon icon="arrow90deg-right"></b-icon>
                    </b-btn>
                    <b-btn id="trash">
                        <b-icon icon="trash"></b-icon>
                    </b-btn>
                    <b-popover target="trash" triggers="click blur" placement="bottom">
                        <b-btn @click="onTrash">Erase All</b-btn>
                    </b-popover>
                    <b-btn @click="onToggleFullscreen">
                        <b-icon v-if="isFullscreen" icon="fullscreen-exit"></b-icon>
                        <b-icon v-else icon="fullscreen"></b-icon>
                    </b-btn>
                </b-row>
            </b-form-group>
        </b-row>
        <div id="canvas-container" class="mx-auto">
            <div id="sheets-container" class="position-absolute">
                <Sheets :textContainers.sync="textContainers" @trimmed="onTextTrimmed"></Sheets>
            </div>
            <canvas class="mt-3" id="canvas" ref="canvas">
            </canvas>
        </div>

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
    BIconCircleFill
} from 'bootstrap-vue'
export default {
    head() {
        return {
            script: [
                {
                    hid: "fabric",
                    src: 'https://unpkg.com/fabric@5.3.0/dist/fabric.min.js',
                    callback: () => {
                        this.setUpCanvas()
                    }
                }
            ]
        }
    },
    components: {
        Verte,
        BIcon,
        BIconArrow90degLeft,
        BIconArrow90degRight,
        BIconTrash,
        BIconFullscreen,
        BIconFullscreenExit,
        BIconArrowLeft,
        BIconCircleFill
    },
    data() {
        return {
            textContainers: [],
            canvas: null,
            brush: null,
            brushColor: "#000000",
            brushColorHistory: ["#4682b4", "#6a5acd", "#ff5733"],
            brushThickness: 1,
            h: [],
            isRedoing: false,
            isFullscreen: false
        }
    },
    computed: {

    },
    methods: {
        setUpCanvas() {
            this.canvas = new fabric.Canvas("canvas", {
                isDrawingMode: true
            })
            this.brush = this.canvas.freeDrawingBrush
            const container = document.querySelector("#sheets-container")
            this.canvas.setDimensions({ width: container.clientWidth, height: container.clientHeight })
            document.querySelector(".canvas-container").style.position = "absolute !important"
            this.canvas.on('object:added', function () {
                if (!this.isRedoing) {
                    this.h = [];
                }
                this.isRedoing = false;
            });
        },
        onTextTrimmed() {
            if (this.canvas) {
                const container = document.querySelector("#sheets-container")
                this.canvas.setDimensions({ width: container.clientWidth, height: container.clientHeight })
                console.log("Text trimmed");
            }
        },
        onColorChange(color) {
            this.canvas.freeDrawingBrush.color = color
            this.brushColor = color
        },
        onThicknessChange(thickness) {
            thickness = parseInt(thickness)
            this.canvas.freeDrawingBrush.width = thickness
            this.brushThickness = thickness
        },
        onUndo() {
            if (this.canvas._objects.length > 0) {
                this.h.push(this.canvas._objects.pop())
                this.canvas.renderAll()
            }
        },
        onRedo() {
            if (this.h.length > 0) {
                this.isRedoing = true;
                this.canvas.add(this.h.pop());
            }
        },
        onTrash() {
            this.$root.$emit('bv::hide::popover', 'trash')
            this.canvas._objects.forEach(o => this.h.push(o))
            this.canvas.clear()
        },
        onToggleFullscreen() {
            if (this.isFullscreen)
                document.exitFullscreen()
            else
                document.body.requestFullscreen()
            this.isFullscreen = !this.isFullscreen
        }
    },
    mounted() {

    }
}
</script>
<style>
#canvas-container {
    position: relative;
    /* width: 11in;
    height: 8.5in; */
}

.canvas-container {
    top: 0;
    left: 0;
    position: absolute !important;
}
</style>