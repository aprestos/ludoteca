<template>
  <l-game-card :game_id="game.id" :loading="loading" :title="game.game.name" :image="game.game.image">
    <template #loading>
      <b-skeleton width="30%"/>
      <div v-if="isAdmin()">
        <b-skeleton width="50%"/>
      </div>
    </template>
    <template #content>
      <div v-if="isAdmin()">
              <div class="d-flex flex-row">
                <div class="d-flex flex-column flex-grow-1">
                  <span class="font-weight-bold">{{ game.selling_price }} €</span>
                  <span class="text-muted">{{ game.stock }} available</span>
                </div>

                <b-dropdown right variant="link" toggle-class="text-decoration-none" no-caret>
                  <template #button-content>
                    <b-icon-three-dots-vertical class="text-dark mr-n3" font-scale="1"/>
                  </template>
                  <b-dropdown-item v-b-modal="`modal-${game.id}`">Update stock</b-dropdown-item>
                  <b-dropdown-item @click="deleteGame(game.id)">Delete</b-dropdown-item>
                </b-dropdown>
              </div>
            </div>

            <div v-else>
              <span v-if="game.is_available" class="font-weight-bold mb-0" style="font-weight: 400">
                {{ game.selling_price }} €
              </span>
              <span v-if="!game.is_available" class="small d-block text-danger">
                Sold out
              </span>
            </div>
      <b-modal :id="`modal-${game.id}`" :title="game.game.name"
               @ok="updateStock">
        <b-form-group class="max-width-2" label="Current">
          <b-form-spinbutton disabled readonly
                             :value="game.stock"
                             size="lg"/>
        </b-form-group>

        <b-form-group class="max-width-2" label="New">
          <b-form-spinbutton
              min="0" v-model="form.stock"
              size="lg"/>
        </b-form-group>

      </b-modal>
    </template>

  </l-game-card>
</template>

<script>
import gamesMixin from '@/mixins/games.mixin'
import usersMixin from '@/mixins/users.mixin'
import storeService from '@/services/store.service'
import LGameCard from "@/components/cards/GameCard"

export default {
  name: 'StoreHomePartialGameCard',
  components: {
    LGameCard
  },
  props: {
    loading: {
      default: false,
      type: Boolean,
    },
    game: {
      default: () => {
        return {
          id: '',
          stock: 0,
          selling_price: 0,
          game: {
            image: '',
            name: '',
          },
          is_available: true
        }
      },
      type: Object,
    },
    selectable: {
      default: false,
      type: Boolean,
    },
    selected: {
      default: false,
      type: Boolean,
    },
  },
  mixins: [gamesMixin, usersMixin],
  data() {
    return {
      form: {
        stock: this.game.stock
      }
    }
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

    associate_discount() {
      let parcel = 1
      const configurations = this.$store.getters['configurations/all']
      if (configurations) {
        const configuration = configurations.filter(conf => conf.key === 'associate_discount')[0]
        parcel = configuration.value
      }
      return parcel
    }
  },
  methods: {
    updateStock() {
      storeService.updateGame(this.game.id, {'stock': this.form.stock}).then((response) => {
        this.$emit('update', response)
      })
    },
    deleteGame(game_id) {
      storeService.deleteGame(game_id).then(() => {
        this.$emit('delete', game_id)
      })
    }
  }
}
</script>

<style scoped></style>
