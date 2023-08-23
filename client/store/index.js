export const state = () => ({
    textOptions: {
        "q": "Romans 8:31-39",
        // q: "Gen 1",
        "include-passage-references": true,
        "include-footnotes": false,
        "include-headings": false,
        "version": "ESV"
    },
    observations: {
        "Repetition": true,
        "Continuity": false,
        "Inclusios": false,
        "Causation": false,
        "Substantiation": false,
        "Comparisons/Contrasts": true,
        "Connectors": true,
        "Structure": true,
        "Preparation/Intro": false,
        "Refrain": false,
        "Explanation/Analysis": false,
        "Summarization": false,
        "Genre": true,
        "Mood": true,
        "Grammar": true,
        "Names/Titles of Characters": true,
        "Climax": true,
        "Other Literary Devices": true,
    },
    questions: {
        Definitive: 0,
        Rational: 0,
        Implicational: 0,
    },
    applications: {
        Head: 0,
        Heart: 0,
        Hands: 0,
    },
    passages: [],
    printable: false,
    downloading: false,
    fontSize: 10,
    lineSpacing: 1.2,
    trimming: false,
    versions: ["ESV", "CSB", "NIV", "KJV", "NKJV"]
})

export const mutations = {
    setTextOption(state, { option, value }) {
        state.textOptions[option] = value
    },
    setObservation(state, { observation, value }) {
        state.observations[observation] = value
    },
    setPassages(state, passages) {
        state.passages = passages
    },
    setPrintable(state, printable) {
        state.printable = printable
    },
    setDownloading(state, downloading) {
        state.downloading = downloading
    },
    setFontSize(state, size) {
        state.fontSize = size
    },
    setLineSpacing(state, spacing) {
        state.lineSpacing = spacing
    },
    setQuestion(state, { question, value }) {
        state.questions[question] = parseInt(value)
    },
    setApplication(state, { application, value }) {
        state.applications[application] = parseInt(value)
    },
    setTrimming(state, trimming) {
        state.trimming = trimming
    }
}

export const actions = {
    async fetchText({ commit, state }) {
        let passages = []
        let query = state.textOptions.q
        await this.$axios.get("text", {
            params: state.textOptions
        })
            .then(res => {
                if (res.data.errors) passages = [`Passage not found.\n${state.textOptions.q}`]
                else if (res.data.passages.length == 0) passages = [`Passage not found.\n${state.textOptions.q}`]
                else {
                    passages = res.data.passages
                    query = res.data.query.replace("\u2013", "-")
                }
            })
            .catch(err => passages = [`Passage not found.\n${state.textOptions.q}`])
        commit("setPassages", passages)
        commit("setTextOption", { option: "q", value: query })
    }
}