import { unauthApi } from '@/services/api'

const URL = '/api/events/'

export default {
  get(id) {
    return unauthApi.get(URL + id + '/').then((response) => response.data)
  },
}
