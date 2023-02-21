import { authApi, unauthApi } from '@/services/api'

const URL = '/api/external-links/'

export default {
  /**
   * Get all links
   * @returns {Promise<AxiosResponse<any>>}
   */
  fetchAll() {
    return unauthApi.get(URL, {}).then((response) => response.data)
  },
  create(payload) {
    return authApi.post(URL, payload).then((response) => response.data)
  },
  update(id, payload) {
    return authApi
      .patch(URL + `${id}/`, payload)
      .then((response) => response.data)
  },
  delete(id) {
    return authApi.delete(URL + `${id}/`).then((response) => response.data)
  },
}
