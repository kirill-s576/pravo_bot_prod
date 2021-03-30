export const state = () => ({
  buttons: [],
  texts: [],
  languages: [],
  langChoices: []
})

export const getters = {
  getButtons (state) {
    return state.buttons
  },
  getTexts (state) {
    return state.texts
  },
  getLanguages (state) {
    return state.languages
  },
  langChoices (state) {
    return state.langChoices
  }
}

export const mutations = {
  SET_BUTTONS (state, buttons) {
    state.buttons = buttons
  },
  SET_TEXTS (state, texts) {
    state.texts = texts
  },
  SET_LANGUAGES (state, languages) {
    state.languages = languages
  },
  SET_LANG_CHOICES(state, langChoices) {
    state.langChoices = langChoices
  },
}

export const actions = {
  setButtons (context) {
    this.$axios.get(
      '/quiz/buttons/'
    )
      .then(
        response => {
          context.commit("SET_BUTTONS", response.data)
        }
      )
  },
  setTexts (context) {
    this.$axios.get(
      '/quiz/messages/'
    )
      .then(
        response => {
          context.commit("SET_TEXTS", response.data)
        }
      )
  },
  setLanguages (context) {
    this.$axios.get(
      '/quiz/languages'
    )
      .then(
        response => {
          context.commit("SET_LANGUAGES", response.data)
        }
      )
  },
  setLangChoices (context) {
    this.$axios.get(
      '/quiz/languages/get_choices/'
    )
      .then(
        response => {
          context.commit("SET_LANG_CHOICES", response.data)
        }
      )
  },

}
