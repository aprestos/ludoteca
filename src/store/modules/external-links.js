import externalLinksService from '@/services/externalLinks.service'

const state = {
  links: [],
}

const getters = {
  all: (state) => {
    return state.links
  },
  get: (state) => (key) => {
    return state.links.filter((config) => (config.key = key))
  },
}

const actions = {
  load({ commit }) {
    externalLinksService.fetchAll().then((response) => {
      commit('setLinks', response)
    })
  },
}

const mutations = {
  setLinks(state, payload) {
    state.links = payload
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
