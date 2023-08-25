<template>
    <div class="canvas-wrapper">
        <canvas :id="id"></canvas>
    </div>
</template>
<script>
export default {
    props: {
        width: {
            type: Number,
            default: 300
        },
        height: {
            type: Number,
            default: 300
        },
        brushColor: String,
        brushWidth: Number
    },
    data() {
        return {
            id: "" + Math.random() * 1000000000,
            canvas: null,
        }
    },
    watch: {
        width(width) {
            this.canvas.setDimensions({ width: width })
        },
        height(height) {
            this.canvas.setDimensions({ height: height })
        },
        brushColor(color) {
            this.canvas.freeDrawingBrush.color = this.brushColor
        },
        brushWidth(width) {
            this.canvas.freeDrawingBrush.width = parseInt(this.brushWidth)
        }
    },
    methods: {
        setUpCanvas() {
            this.canvas = new fabric.Canvas(this.id, {
                isDrawingMode: true
            })
            this.canvas.setDimensions({ width: this.width, height: this.height })
            this.canvas.freeDrawingBrush.color = this.brushColor
            this.canvas.freeDrawingBrush.width = parseInt(this.brushWidth)
            // this.canvas.on('object:added', function () {
            //     if (!this.isRedoing) {
            //         this.h = [];
            //     }
            //     this.isRedoing = false;
            // });
        }
    },
    mounted() {
        this.setUpCanvas()
    }
}
</script>
<style scoped>
.canvas-wrapper {
    position: absolute;
    left: 0;
    top: 0;
}
</style>