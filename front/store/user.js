export const state = () => ({
  userData: null,
  token: null,
})

export const getters = {
  userData ( state ) {
    return state.userData
  },
  token ( state ) {
    return state.token
  }
}

export const mutations = {
  SET_USER_DATA (state, userData) {
    state.userData = userData
  },
  SET_TOKEN (state, token) {
    state.token = token
  },
  LOGOUT ( state ) {
    state.userData = null
    state.token = null
  }
}

export const actions = {
  refreshUserData ( context ) {
    this.$axios.get(
      '/auth/user/mine_get/'
    )
      .then(response => {
        context.commit('SET_USER_DATA', response.data)
      })
  },
  async login ( context, { email, password} ) {
    const {
      data: {
        refresh, access
      }
    } = await this.$axios.post(
      '/auth/token',
      {
        email: email,
        password: password
      }
    )
    context.commit('SET_TOKEN', access)
  },
  logout ( context ) {
    context.commit ('LOGOUT')
  }
}
