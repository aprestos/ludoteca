import authorizationService from '@/services/authorization.service'

export default {
  methods: {
    isAuthenticated: function() {
      return authorizationService.isAuthenticated()
    },
    isAdmin: function(){
      return this.$store.getters["users/current"].is_staff
    }
  },
}
