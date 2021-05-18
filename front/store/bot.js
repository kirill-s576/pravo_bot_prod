export const state = () => ({
  botLanguages: [],
  langChoices: [],
  botMessages: []
})

export const getters = {
  botLanguages ( state ) {
    return state.botLanguages
  },
  botMessages ( state ) {
    return state.botMessages
  },
  langChoices ( state ) {
    return state.langChoices
  }
}

export const mutations = {
  SET_BOT_LANGUAGES (state, botLanguages) {
    state.botLanguages = botLanguages
  },
  SET_BOT_MESSAGES(state, botMessages) {
    state.botMessages = botMessages
  },
  SET_BOT_LANGUAGE_CHOICES(state, langChoices) {
    state.langChoices = langChoices
  }
}

export const actions = {
  refreshBotLanguages ( context ) {
    this.$axios.get(
      '/tg_bot/languages/'
    )
      .then(response => {
        context.commit('SET_BOT_LANGUAGES', response.data)
      })
  },
  refreshBotMessages ( context ) {
    this.$axios.get(
      '/tg_bot/messages/'
    )
      .then(response => {
        context.commit('SET_BOT_MESSAGES', response.data)
      })
  },
  refreshLangChoices ( context ) {
    this.$axios.get(
      '/tg_bot/languages/get_choices/'
    )
      .then(response => {
        context.commit('SET_BOT_LANGUAGE_CHOICES', response.data)
      })
  },
}
