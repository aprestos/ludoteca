<template>
  <HomeScreenTemplate :title="title" :pre-title="pretitle">
    <template #actions>
      <b-button
        class="d-inline-block ml-3"
        v-if="isStaff()"
        variant="primary"
        :to="{ name: 'StoreAddGame' }"
        >Add game</b-button
      >
    </template>
    <b-row class="mb-3">
      <!-- Search -->
      <b-col>
        <l-search v-model="search" />
      </b-col>
      <FiltersButton :filters="filters" collapse-id="store-filters" />
    </b-row>
    <Filters
      v-model="filters"
      collapse-id="store-filters"
      :sort-options="[
        { value: 'game__name', text: 'Name' },
        { value: 'game__year,game__name', text: 'Year' },
        { value: 'selling_price', text: 'Price' },
        { value: 'game__rank', text: 'BGG Rank' },
      ]"
    >
    </Filters>

    <Games
      :loading="loading"
      :games="games"
      @update="updateGame"
      class="pt-5"
      @delete="deleteGame"
    />

    <Pagination :current-page="currentPage" :total-count="totalGamesCount" @page-changed="pageChanged"/>
  </HomeScreenTemplate>
</template>

<script>
import Games from '@/pages/store/home/partials/Games'
import HomeScreenTemplate from '@/components/templates/HomeScreenTemplate'
import storeService from '@/services/store.service'
import usersMixin from '@/mixins/users.mixin'
import Pagination from '@/components/Pagination'
import LSearch from '@/components/form/LSearch'
import FiltersButton from '@/components/filters/FiltersButton'
import Filters from '@/components/filters/Filters'

export default {
  name: 'StoreHome',
  components: {
    FiltersButton,
    HomeScreenTemplate,
    Games,
    Pagination,
    LSearch,
    Filters,
  },
  mixins: [usersMixin],
  props: ['title', 'pretitle'],
  data() {
    return {
      search: '',
      filters: new Filters.Model(),
      currentPage: 1,
      games: [],
      loading: true,
      totalGamesCount: 0,
    }
  },
  mounted() {
    this.refreshGames()
  },
  computed: {
    associate_discount() {
      const configurations = this.$store.getters['configurations/all']
      if (configurations) {
        return configurations.filter(
          (conf) => conf.key === 'associate_discount',
        )[0].value
      }
      return 1
    },
  },
  watch: {
    search() {
      // anytime the search string is change we should reset page number
      // otherwise the user could face a 404 because the page is not available for the search results
      this.currentPage = 1

      this.refreshGames()
    },
    filters: {
      handler: function () {
        this.refreshGames()
      },
      deep: true,
    },
  },
  methods: {
    getParams() {
      let params = {}

      params['page'] = this.currentPage

      if (this.search) {
        params['search'] = this.search
      }

      if(this.filters.sortBy){
        if(this.filters.sortBy.fields){

          if(this.filters.sortBy.order === 'asc'){
            params['ordering'] = this.filters.sortBy.fields
          } else if(this.filters.sortBy.order === 'desc'){
            params['ordering'] = `-${this.filters.sortBy.fields}`
          }
        }
      }

      return params
    },
    refreshGames() {
      let params = this.getParams()
      this.loading = true
      storeService.filterGames(params).then((response) => {
        this.games = response.results
        this.loading = false
        this.totalGamesCount = response.count
      })
    },
    updateGame(game) {
      if (game) {
        const outdatedGameObject = this.games.filter(
          (item) => item.id === game.id,
        )[0]
        this.$set(this.games, this.games.indexOf(outdatedGameObject), game)
      } else {
        storeService
          .fetchGames(this.currentPage)
          .then((response) => (this.games = response))
      }
    },
    deleteGame(game_id) {
      if (game_id) {
        const outdatedGameObject = this.games.filter(
          (item) => item.id === game_id,
        )[0]
        this.games.splice(this.games.indexOf(outdatedGameObject), 1)
      } else {
        storeService
          .fetchGames(this.currentPage)
          .then((response) => (this.games = response))
      }
    },
    pageChanged(page){
      this.currentPage = page
      this.refreshGames()
    }
  },
}
</script>

<style scoped></style>
