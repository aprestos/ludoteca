<template>
  <HomeScreenTemplate :pre-title="pretitle" :title="title">
    <template #actions>
      <div v-if="isStaff()">
        <b-dropdown class="mr-3" no-caret variant="white">
          <template #button-content>
            <b-icon-gear />
          </template>
          <b-dropdown-item-button v-show="!bulk" @click="bulk = true">
            Enable God mode
          </b-dropdown-item-button>
          <b-dropdown-item-button v-show="bulk" @click="bulk = false">
            Disable God mode
          </b-dropdown-item-button>
        </b-dropdown>

        <b-button v-if="isStaff()" :to="{ name: 'AddLibraryGame' }" variant="primary">
          <b-icon-plus class="mr-2" />
          Add game
        </b-button>
      </div>
    </template>

    <!-- Search and filters trigger -->
    <b-row class="align-items-center mb-3">
      <!-- Search -->
      <b-col>
        <l-search v-model="search" />
      </b-col>

      <FiltersButton :filters="filters" collapse-id="filters-collapse" />
    </b-row>

    <!-- Filters -->
    <Filters
      v-model="filters"
      collapse-id="filters-collapse"
      :sort-options="[
        { value: 'game__name', text: 'Name' },
        { value: 'game__year,game__name', text: 'Year' },
        { value: 'num_withdraws', text: 'Requisitions' },
        { value: 'game__rank', text: 'Rank' },
        { value: 'game__weight', text: 'Complexity' },
      ]"
      @filter-change="filtersChange"
    >
      <FilterSelect
        v-if="isStaff()"
        id="location"
        v-model="filters"
        :options="$store.getters['library/locations']"
        label="Location"
      />
      <FilterSelect
        v-if="isStaff()"
        id="owner"
        v-model="filters"
        :options="$store.getters['library/players']"
        label="Owner"
        @search="searchPlayers"
      />
      <FilterRadioButton
        id="status"
        v-model="filters"
        label="Status"
        :options="[
          { text: 'Available', value: 'available' },
          { text: 'Playing', value: 'not-available' },
          { text: 'Not checked-in', value: 'not-checked-in' },
        ]"
      />
      <div class="d-flex flex-row">
        <FilterRange id="players" class="mr-2" label="Players" v-model="filters" />
        <FilterRange id="playtime" class="ml-2" label="Playtime" v-model="filters"/>
      </div>
    </Filters>

    <!-- Content -->
    <div class="mt-5">
      <b-row>
        <!-- Games list -->
        <b-col
          v-for="(game, index) in games"
          :key="index"
          class="d-flex"
          cols="6"
          lg="2"
          md="3"
          sm="4"
        >
          <Game
            :game="game"
            :is-bulk-enabled="bulk"
            :loading="loading"
            :selectable="isGameSelectable(game)"
            :selected="selected.includes(game.id)"
            @return="refreshGames"
            @selected-change="updateSelected"
            @check-in="openLocationModal"
          >
          </Game>
        </b-col>
      </b-row>

      <CheckinModal
        id="checkin-modal"
        :game="selectedGame"
        :shelves="$store.getters['library/locations']"
        @done="updateGame($event)"
      />
    </div>

    <Pagination :current-page="currentPage" :total-count="totalGamesCount" @page-changed="pageChanged" />

    <div
      class="list-alert alert alert-dark alert-dismissible border fade"
      role="alert"
      v-bind:class="{ show: bulk }"
    >
      <!-- Content -->
      <div class="row align-items-center">
        <div class="col">
          <!-- Checkbox -->
          <div class="custom-control custom-checkbox">
            <input
              id="listAlertCheckbox"
              checked=""
              class="custom-control-input"
              disabled=""
              type="checkbox"
            />
            <label
              class="custom-control-label text-white"
              for="listAlertCheckbox"
              ><span class="list-alert-count">{{ selected.length }}</span>
              game(s)</label
            >
          </div>
        </div>
        <div class="col-auto mr-n3">
          <!-- Button -->
          <!--          <b-button-->
          <!--            v-if="games.length > selected.length"-->
          <!--            class="btn-white-20"-->
          <!--            size="sm"-->
          <!--            @click="selectAll"-->
          <!--          >-->
          <!--            Select all-->
          <!--          </b-button>-->
          <!--          <b-button-->
          <!--            v-else-->
          <!--            class="btn-outline-white"-->
          <!--            size="sm"-->
          <!--            @click="unselectAll"-->
          <!--          >-->
          <!--            Unselect all-->
          <!--          </b-button>-->
          <b-dropdown
            :disabled="selected.length === 0"
            class="ml-3"
            dropup
            no-caret
            size="sm"
            variant="white-20"
          >
            <template #button-content>
              <div class="d-flex flex-row align-items-center">
                Actions
                <b-icon-caret-up-fill
                  class="ml-2"
                  font-scale="0.8"
                ></b-icon-caret-up-fill>
              </div>
            </template>
            <b-dropdown-item-button @click="deleteGames"
              >Remove
            </b-dropdown-item-button>
            <b-dropdown-item-button @click="checkoutGames"
              >Checkout
            </b-dropdown-item-button>
          </b-dropdown>
        </div>
      </div>
      <!-- / .row -->

      <!-- Close -->
      <button
        aria-label="Close"
        class="list-alert-close close"
        type="button"
        @click="bulk = false"
      >
        <span aria-hidden="true">×</span>
      </button>
    </div>

    <ModalPlayerSelect id="filter-players-modal"></ModalPlayerSelect>
  </HomeScreenTemplate>
</template>

<script>
import gamesMixin from '@/mixins/games.mixin'
import libraryService from '@/services/library.service'
import ModalPlayerSelect from '@/components/ModalPlayerSelect'
import playerService from '@/services/player.service'
import CheckinModal from '@/components/CheckinModal'
import usersMixin from '@/mixins/users.mixin'
import axiosUtils from '@/mixins/axios.utils'
import Pagination from '@/components/Pagination'
import Filters from '@/components/filters/Filters'
import FiltersButton from '@/components/filters/FiltersButton'
import FilterSelect from '@/components/filters/FilterSelect'
import HomeScreenTemplate from '@/components/templates/HomeScreenTemplate'
import Game from './partials/Game'
import FilterRadioButton from '@/components/filters/FilterRadioButton'
import LSearch from '@/components/form/LSearch'
import FilterRange from "@/components/filters/FilterRange.vue"

export default {
  name: 'Home',
  props: ['title', 'pretitle'],
  data() {
    return {
      search: '',
      games: new Array(6).fill({
        game: { name: '', image: '' },
        owner: { name: '' },
        id: 0,
      }),
      loading: true,
      bulk: false,
      selected: [],
      selectedGame: {
        game: {},
      },
      selectedGames: [],
      players: [],
      filters: new Filters.Model(),
      availability_options: [],
      status_options: [
        { value: 'available', text: 'Available' },
        { value: 'not-available', text: 'Withdrawn' },
        { value: 'not-checked-in', text: 'Not checked-in' },
        { value: 'checked-out', text: 'Checked-out' },
      ],
      currentPage: 1,
      totalGamesCount: 0,
    }
  },
  components: {
    FilterRange,
    LSearch,
    FilterRadioButton,
    HomeScreenTemplate,
    FiltersButton,
    Pagination,
    CheckinModal,
    ModalPlayerSelect,
    Game,
    Filters,
    FilterSelect,
  },
  mixins: [gamesMixin, usersMixin],
  created() {
    this.refreshGames()
  },
  methods: {
    selectAll() {
      const availableGames = this.games.filter((game) =>
        this.isGameSelectable(game),
      )

      availableGames.forEach((game) => this.updateSelected(game.id))
    },
    unselectAll() {
      this.selected = []
    },
    refreshGames() {
      this.loading = true

      let params = this.getParams()

      libraryService.filterGames(params).then((response) => {
        this.games = response.results
        this.totalGamesCount = response.count
        this.loading = false
      })
    },
    searchPlayers(query) {
      playerService.searchPlayers(query).then((response) => {
        this.players = response
      })
    },
    checkoutGames() {
      let promises = this.selected.map((id) => libraryService.checkoutGame(id))

      Promise.all(promises)
        .then(() => {
          this.$toast.success(
            `Checked-out ${promises.length} ${
              this.selected.length > 1 ? 'games' : 'game'
            }`,
          )
        })
        .catch((response) => {
          this.$toast.error(
            'Error checking-out game(s): ' +
              axiosUtils.getErrorDescription(response),
          )
        })
        .finally(() => {
          this.bulk = false
          this.unselectAll()
          this.refreshGames()
        })
    },
    deleteGames() {
      const isOwnerLeiriaCon = this.games.filter(
        (game) =>
          game.owner.name === 'leiriacon' && this.selected.includes(game.id),
      ).length

      if (isOwnerLeiriaCon) {
        this.$bvModal
          .msgBoxConfirm(
            'The selected games will be removed from the library. Do you want to continue?',
            {
              title: 'Are you sure?',
              okVariant: 'danger',
              okTitle: 'Yes',
              cancelTitle: 'No',
            },
          )
          .then((confirmed) => {
            if (confirmed) {
              this.deleteSelectedGames()
            }
          })
          .catch((error) =>
            this.$toast.error('Error checking-out game(s): ' + error),
          )
      } else {
        this.deleteSelectedGames()
      }
    },
    deleteSelectedGames() {
      let promises = this.selected.map((id) => libraryService.deleteGame(id))

      Promise.all(promises)
        .then(() => {
          this.$toast.success(
            `Deleted ${promises.length} ${
              this.selected.length > 1 ? 'games' : 'game'
            }`,
          )
        })
        .catch((response) => {
          this.$toast.error(
            'Error deleting game(s): ' +
              axiosUtils.getErrorDescription(response),
          )
        })
        .finally(() => {
          this.bulk = false
          this.unselectAll()
          this.refreshGames()
        })
    },
    getParams() {
      let params = {}

      params['page'] = this.currentPage

      if (this.search) {
        params['search'] = this.search
      }
      params['page_size'] = this.$store.getters["pagination/pageSize"]

      if (this.filters.sortBy) {
        if (this.filters.sortBy.fields) {
          if (this.filters.sortBy.order === 'asc') {
            params['ordering'] = this.filters.sortBy.fields
          } else if (this.filters.sortBy.order === 'desc') {
            params['ordering'] = `-${this.filters.sortBy.fields}`
          }
        }
      }

      Object.keys(this.filters.filtersSelected).forEach(
        (key) => (params[key] = this.filters.filtersSelected[key]),
      )

      return params
    },
    openLocationModal(game) {
      this.selectedGame = game
      this.$bvModal.show('checkin-modal')
    },
    updateSelected(game_id) {
      if (this.selected.includes(game_id)) {
        this.selected.splice(this.selected.indexOf(game_id), 1)
      } else {
        this.selected.push(game_id)
      }
    },
    isGameSelectable(game) {
      return this.bulk && game.status === 'available'
    },
    updateGame(game) {
      if (game) {
        const outdatedGameObject = this.games.filter(
          (item) => item.id === game.id,
        )[0]
        this.$set(this.games, this.games.indexOf(outdatedGameObject), game)
      }
    },
    filtersChange(filters) {
      this.filters = filters
    },
    pageChanged(page){
      this.currentPage = page
      this.refreshGames()
    }
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
}
</script>
<style lang="scss"></style>
