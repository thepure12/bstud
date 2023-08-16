export const state = () => ({
    textOptions: {
        "q": "Romans 8:31-39",
        "include-passage-references": true,
        "include-footnotes": false,
        "include-headings": false
    },
    observations: [
        {
            "Repeated Words": true,
            "Comparisons and Contrasts": true,
            "Connectors": true,
            "Structure": true,
        },
        {
            "Genre": true,
            "Mood": true,
            "Grammar": true,
            "Names/Titles of Characters": true,
            "Climax": true,
            "Other Literary Devices": true,
        }
    ],
    passages: [],
    printable: false,
    fontSize: 10
})

export const mutations = {
    setTextOption(state, { option, value }) {
        state.textOptions[option] = value
    },
    setObservation(state, { col, observation, value }) {
        state.observations[col][observation] = value
    },
    setPassages(state, passages) {
        state.passages = passages
    },
    setPrintable(state, printable) {
        state.printable = printable
    },
    setFontSize(state, size) {
        state.fontSize = size
    }
}

export const actions = {
    async fetchText({ commit, state }) {
        let passages = []
        await this.$axios.get("text", {
            params: state.textOptions
        })
            .then(res => {
                if (res.data.errors) passages = [`Passage not found.\n${state.textOptions.q}`]
                else if (res.data.passages.length == 0) passages = [`Passage not found.\n${state.textOptions.q}`]
                else passages = res.data.passages
            })
            .catch(err => passages = [`Passage not found.\n${state.textOptions.q}`])
        commit("setPassages", passages)
    }
}