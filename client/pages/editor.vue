<template>
    <div class="m-3 ">
        <b-row v-if="canvas" class="mb-3 justify-content-around border-bottom">
            <b-form-group label="Color">
                <verte picker="square" :value="canvas.freeDrawingBrush.color" @input="onColorChange"></verte>
            </b-form-group>
            <b-form-group label="Thickness" :style="`border-bottom: ${brushThickness}px solid ${brushColor}`">
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
                </b-row>
            </b-form-group>
        </b-row>
        <div id="canvas-container" class="mx-auto">
            <div class="position-absolute">
                <Sheets :textContainers.sync="textContainers"></Sheets>
            </div>
            <canvas class="mt-3" id="canvas" ref="canvas">
            </canvas>
        </div>

    </div>
</template>
<script>
import Verte from 'verte';
import 'verte/dist/verte.css';
import { BIcon, BIconArrow90degLeft, BIconArrow90degRight, BIconTrash } from 'bootstrap-vue'
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
        BIconTrash
    },
    data() {
        return {
            textContainers: [],
            canvas: null,
            brush: null,
            brushColor: "black",
            brushThickness: 1,
            h: [],
            isRedoing: false,
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
            const container = document.querySelector("#canvas-container")
            this.canvas.setDimensions({ width: container.clientWidth, height: container.clientHeight })
            document.querySelector(".canvas-container").style.position = "absolute !important"
            this.canvas.on('object:added', function () {
                if (!this.isRedoing) {
                    this.h = [];
                }
                this.isRedoing = false;
            });
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
        }
    },
    mounted() {

    }
}
</script>
<style>
#canvas-container {
    position: relative;
    width: 11in;
    height: 8.5in;
}

.canvas-container {
    top: 0;
    left: 0;
    position: absolute !important;
}
</style>