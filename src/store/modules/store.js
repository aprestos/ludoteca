const state = {
  suppliers: [],
}

const getters = {
  suppliers: (state) => {
    return state.suppliers
  },
}

const actions = {
  loadSuppliers() {
    //supplierService.fetchAll().then(data => {
    //  commit('setSuppliers', data)
    //})
  },
}

const mutations = {
  setSuppliers(state, payload) {
    state.suppliers = payload
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations,
}
