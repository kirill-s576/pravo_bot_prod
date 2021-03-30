export const state = () => ({
  stagesTree: null
})

export const getters = {
  getStagesTree (state) {
    return state.stagesTree
  }
}

export const mutations = {
  SET_STAGES_TREE (state, tree) {
    state.stagesTree = tree
  }
}

export const actions = {
  setStagesTree (context) {
    this.$axios.get(
      '/quiz/stages/tree'
    )
      .then(
        response => {
          context.commit("SET_STAGES_TREE", response.data)
        }
      )
  }
}
