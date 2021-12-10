import { authApi } from '@/services/api'

const URL = '/api/dashboard/'

export default {
  /**
   * Get dashboard content
   * @returns {Promise<*>}
   */
  getContent() {
    return authApi
      .get(URL)
      .then(response => response.data)
  },

}
