<template>
    <div class="m-3 ">
        <b-row v-if="canvas" class="mb-3 justify-content-around">
            <b-form-group label="Color">
                <verte picker="square" :value="canvas.freeDrawingBrush.color" @input="onColorChange"></verte>
            </b-form-group>
            <b-form-group label="Thickness" :style="`border-bottom: ${brushThickness}px solid ${brushColor}`">
                <b-form-input type="range" :value="canvas.freeDrawingBrush.width" @input="onThicknessChange" min="1"
                    max="50" step="1"></b-form-input>
            </b-form-group>
            <b-form-group class="my-auto">
                <b-btn @click="onUndo">Undo</b-btn>
            </b-form-group>
        </b-row>
        <div id="canvas-container" class="mx-auto">
            <div class="m-3 position-absolute">
                {{ $store.state.passages[0] }}
            </div>
            <canvas class="border" id="canvas" ref="canvas">
            </canvas>
        </div>

    </div>
</template>
<script>
import Verte from 'verte';
import 'verte/dist/verte.css';

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
        Verte
    },
    data() {
        return {
            canvas: null,
            brush: null,
            brushColor: "black",
            brushThickness: 1,
            suckerCanvas: null,
            suckerArea: [],
            isSucking: false
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
        },
        onColorChange(color) {
            // const { r, g, b, a } = color.rgba
            // this.canvas.freeDrawingBrush.color = `rgba(${r}, ${g}, ${b}, ${a})`
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
                this.canvas._objects.pop()
                this.canvas.renderAll()
            }
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