<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light" id="topnav">
      <div class="container">
        <!-- Toggler -->
        <b-navbar-toggle class="navbar-toggler me-auto collapsed" target="nav-collapse"/>

        <!-- Brand -->
        <b-link :to="{'name': 'Home'}" class="navbar-brand me-auto">
          <img src="@/assets/leiriacon_new.png" alt="..." class="navbar-brand-img">
        </b-link>


        <!-- User -->
        <div class="navbar-user">
          <!-- Dropdown -->
          <div class="dropdown" v-if="isAuthenticated()">

            <!-- Toggle -->
            <a  href="#" class="avatar avatar-sm dropdown-toggle" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <b-avatar :text="initials($store.getters['users/current'].name)" variant="dark"/>
            </a>

            <!-- Menu -->
            <div class="dropdown-menu dropdown-menu-right">
              <div class="dropdown-item-text d-flex justify-content-between row" v-if="isAssociate()">
                <span class="text-dark ml-3">Quotas</span>
                <Quotas class="mr-3" :quotas="$store.getters['users/current'].quotas"/>
              </div>
              <hr v-if="isAssociate()" class="dropdown-divider"/>
              <b-link v-if="isStaff()" :to="{'name': 'Dashboard'}" class="dropdown-item">Dashboard</b-link>
              <b-link v-if="isAdmin()" :to="{'name': 'Configurations'}" class="dropdown-item">Configurations</b-link>
              <hr v-if="isStaff() || isAdmin()" class="dropdown-divider">
              <b-link @click="logout" class="dropdown-item">Logout</b-link>
            </div>
          </div>
          <b-link v-if="!isAuthenticated()" :to="{'name': 'Login'}">Sign in</b-link>
        </div>

        <!-- Collapse -->
        <b-collapse id="nav-collapse" class="navbar-collapse me-lg-auto order-lg-first collapse">
          <!-- Navigation -->
          <b-navbar-nav>
            <b-nav-item :to="{ name: 'LibraryHome' }" active-class="active">
              Library
            </b-nav-item>
            <b-nav-item v-if="hasPermission(game_permissions.Store.View)" :to="{ 'name': 'StoreHome' }" active-class="active">
              Store
            </b-nav-item>
            <b-nav-item v-if="hasPermission(user_permissions.Add)" :to="{ 'name': 'PlayersHome' }" active-class="active">
              Players
            </b-nav-item>
            <b-nav-item :to="{ name: 'Tickets' }" active-class="active">
              Tickets
            </b-nav-item>
            <b-nav-item-dropdown toggle-class="nav-link dropdown-toggle" v-show="$store.getters['externalLinks/all'].length" text="Useful links">
              <b-dropdown-item
                  v-for="(link, index) in $store.getters['externalLinks/all']"
                  v-bind:key="index"
                  :href="link.url" target="_blank">
                {{link.text}}
              </b-dropdown-item>
            </b-nav-item-dropdown>
          </b-navbar-nav>
        </b-collapse>

      </div> <!-- / .container -->
    </nav>

    </div>
</template>
<script>
import usersMixin from '@/mixins/users.mixin'
import authorizationService from '@/services/authorization.service'
import {GamePermissions, UserPermissions} from '@/enums/permissions.enum'
import {max} from "@/utils/number.utils"
import Quotas from "@/components/user/Quotas.vue"
import personMixin from "@/mixins/person.mixin"

export default {
  name: 'TopNav',
  components: {Quotas},
  mixins: [usersMixin, personMixin],
  data(){
    return {
      game_permissions: GamePermissions,
      user_permissions: UserPermissions
    }
  },
  methods: {
    logout() {
      authorizationService.logout()
      location.reload()
    },
  },
  computed: {
    numberOfQuotasDue() {
      return this.getNumberOfQuotasDue(this.$store.getters["users/current"].quotas)
    },
    lastPaidQuota(){
      return max(this.$store.getters["users/current"].quotas)
    }
  }
}
</script>
