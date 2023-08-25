<template>
    <div>
        <b-row class="mb-3 justify-content-around" :style="`border-bottom: ${brushWidth}px solid ${brushColor}`">
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
                <b-form-input type="range" :value="brushWidth" @input="onThicknessChange" min="1" max="50"
                    step="1"></b-form-input>
            </b-form-group>
            <b-form-group class="my-auto">
                <b-row class="gap-1">
                    <!-- <b-btn @click="onErase">
                        <b-icon icon="eraser"></b-icon>
                    </b-btn> -->
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
        <Sheets :textContainers.sync="textContainers" :drawing="true" :brushColor="brushColor" :brushWidth="brushWidth">
        </Sheets>
    </div>
</template>
<script>
import Verte from 'verte';
import 'verte/dist/verte.css';
import { mapState, mapMutations } from 'vuex'
import {
    BIcon,
    BIconArrow90degLeft,
    BIconArrow90degRight,
    BIconTrash,
    BIconFullscreen,
    BIconFullscreenExit,
    BIconArrowLeft,
    BIconCircleFill,
    BIconEraser
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
        BIconEraser
    },
    data() {
        return {
            textContainers: [],
            brushColor: "#000000",
            brushColorHistory: ["#4682b4", "#6a5acd", "#ff5733"],
            brushWidth: 1,
            h: [],
            isRedoing: false,
            isFullscreen: false
        }
    },
    computed: {
    },
    methods: {
        onSetBrush(brush) {

        },
        onColorChange(color) {
            this.brushColor = color
        },
        onThicknessChange(thickness) {
            thickness = parseInt(thickness)
            this.brushWidth = thickness
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
    mounted() {
    }
}
</script>