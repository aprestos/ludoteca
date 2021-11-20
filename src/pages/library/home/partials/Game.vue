<template>
  <l-game-card :image="game.game.image" :loading="loading" :selected="selected" :title="game.game.name"
               game_id="game.id">

    <template #loading>
      <b-skeleton width="40%"/>
      <b-skeleton width="50%"/>
    </template>
    <template #content>

      <div v-if="isAdmin()">
        <metadata-item class="text-muted" :text="game.owner.name" icon="briefcase-fill"/>
        <metadata-item
            v-bind:class="{ 'text-danger': !game.location, 'text-muted': game.location }"
            :text="game.location ? game.location.name : 'Not available'"
            icon="geo-fill"
        />
        <metadata-item
            class="text-warning"
            v-if="game.status === 'not-available'"
            :text="`${game.current_withdraw.requisitor.name} (${playingTime(new Date(game.current_withdraw.date_withdrawn))})`" icon="person-fill"/>
        <div class="mt-3">
          <div v-if="!isBulkEnabled" class="w-100 d-flex flex-row">
            <div class="flex-grow-1">
              <b-button v-if="game.status === 'not-available'"
                        block
                        size="sm"
                        variant="white"
                        @click="returnGame(game)">
                Return
              </b-button>
              <b-button v-if="game.status === 'not-checked-in'"
                        block
                        size="sm"
                        variant="white"
                        @click="$emit('check-in', game)"
              >
                Check-in
              </b-button>
              <b-button
                  v-if="game.status === 'available'"
                  :to="{ name: 'WithdrawGame', params: { id: game.id } }" block size="sm"
                  variant="light">
                Withdraw
              </b-button>

              <div v-else></div>
            </div>
            <div class="ml-1">
              <b-dropdown dropleft no-caret size="sm" toggle-class="text-decoration-none" variant="light">
                <template #button-content>
                  <b-icon-three-dots-vertical font-scale="1"/>
                </template>
                <b-dropdown-item @click="$emit('check-in', game)">Change location</b-dropdown-item>

              </b-dropdown>
            </div>
          </div>
          <div v-else>
            <b-button v-if="game.status === 'available'" :pressed.sync="gameSelected" block size="sm"
                      variant="outline-dark">
          <span v-if="gameSelected" class="d-flex align-items-center justify-content-center">
          <b-icon-x-circle class="mr-3" font-scale="0.9"/>
            Remove selection
          </span>
              <span v-else class="d-flex align-items-center justify-content-center">
          <b-icon-check-circle-fill class="mr-3" font-scale="0.9"/>
            Select
          </span>
            </b-button>
          </div>
        </div>
      </div>

      <div v-else class="flex flex-column">
        <MetadataItem
            class="text-muted"
            :text="num_players(game.game.min_players, game.game.max_players)"
            icon="person-fill"
        />
        <metadata-item
            class="text-muted"
            :text="playtime(game.game.min_playtime, game.game.max_playtime)"
            icon="clock-fill"
        />
        <metadata-item v-if="game.status === 'not-checked-in'" icon="exclamation-circle-fill" text="Not available" class="text-danger">

        </metadata-item>
        <metadata-item class="text-warning" v-if="game.status === 'not-available'"
                       :text="`Playing (${playingTime(new Date(game.current_withdraw.date_withdrawn))})`" icon="person-fill"/>
      </div>

    </template>
  </l-game-card>

</template>

<script>
import gamesMixin from '@/mixins/games.mixin'
import MetadataItem from '@/components/cards/MetadataItem'
import withdrawService from "@/services/withdraw.service"
import libraryService from "@/services/library.service"
import usersMixin from "@/mixins/users.mixin"
import LGameCard from "@/components/cards/GameCard"

export default {
  name: 'LibraryHomeGameCard',
  props: {
    game: {
      type: Object,
      default: () => {
        return {
          id: '',
          game: {
            min_players: 0,
            max_players: 0,
            min_playtime: 0,
            max_playtime: 0,
          },
          current_withdraw: {
            requisitor: {
              name: '',
            },
          },
        }
      },
    },
    loading: {
      default: false,
      type: Boolean,
    },
    title: {
      default: '',
      type: String,
    },
    image: {
      default: '',
      type: String,
    },
    noFooter: {
      default: false,
      type: Boolean,
    },
    noImage: {
      default: false,
      type: Boolean,
    },
    selectable: {
      default: false,
      type: Boolean,
    },
    selected: {
      default: false,
      type: Boolean,
    },
    isBulkEnabled: {
      default: false,
      type: Boolean
    }
  },
  mixins: [gamesMixin, usersMixin],
  components: {
    MetadataItem, LGameCard
  },
  computed: {
    gameSelected: {
      get() {
        return this.selected
      },
      // eslint-disable-next-line no-unused-vars
      set(val) {
        this.$emit('selected-change', this.game.id)
      },
    },
  },
  methods: {
    returnGame(game) {
      withdrawService.returnGame(game.current_withdraw.id).then(() => {
        this.$toast.success(`Thank you! Place the game on ${game.location.name}`)
        libraryService.fetchGame(game.id).then(() => {
          this.$emit('return')
        })
      })
    },
    playingTime(date){
      const now = new Date()
      const diff = Math.abs(now-date)

      let
          minutes = Math.floor((diff / (1000 * 60)) % 60),
          hours = Math.floor((diff / (1000 * 60 * 60)) % 24)

  hours = (hours < 10) ? "0" + hours : hours
  minutes = (minutes < 10) ? "0" + minutes : minutes

  return hours + ":" + minutes
    }
  },

}
</script>

<style scoped></style>
