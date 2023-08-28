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
        brushWidth: Number,
        erasing: Boolean,
        typing: Boolean
    },
    data() {
        return {
            id: "" + Math.random() * 1000000000,
            canvas: null,
            _brush: null,
            isEditingText: false,
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
            if (this.typing) {
                let activeOvject = this.canvas.getActiveObject()
                if (activeOvject)
                    activeOvject.set({ fill: color })
                this.canvas.renderAll()
            }
        },
        brushWidth(width) {
            this.canvas.freeDrawingBrush.width = parseInt(this.brushWidth)
            if (this.typing) {
                let activeOvject = this.canvas.getActiveObject()
                if (activeOvject)
                    activeOvject.set({ fontSize: width })
                this.canvas.renderAll()
            }
        },
        erasing(erasing) {
            if (erasing) {
                this._brush = this.canvas.freeDrawingBrush
                this.canvas.freeDrawingBrush = new fabric.EraserBrush(this.canvas)
            } else {
                this.canvas.freeDrawingBrush = this._brush
            }
        },
        typing(typing) {
            if (typing) {
                this.canvas.isDrawingMode = false;
            } else {
                this.canvas.isDrawingMode = true;
                // this.canvas.freeDrawingBrush = this._brush
            }
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
            this.canvas.on("object:added", (object) => {
                this.$emit("objectAdded", this.canvas)
            })
            this.canvas.on("erasing:end", (object) => {
                this.$emit("objectErased", this.canvas)
            })
            this.canvas.on("mouse:up", (event) => {
                if (this.typing) {
                    if (event.target && event.target.type === "textbox") {
                        this.isEditingText = true
                    } else {
                        if (!this.isEditingText) {
                            const text = new fabric.Textbox("Tap to edit\n", {
                                editable: true,
                                fontSize: this.brushWidth,
                                fontFamily: "Arial",
                                fill: this.brushColor,
                                width: 250,
                                left: event.pointer.x,
                                top: event.pointer.y,
                                lockScalingY: true,
                                padding: 10
                            })
                            text.setCoords()
                            this.canvas.add(text)
                            this.canvas.setActiveObject(text)
                        } else this.isEditingText = false
                    }
                }
            })
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