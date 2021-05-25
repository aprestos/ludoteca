<template>
  <b-skeleton-wrapper :loading="loading">
    <template #loading>
      <b-card no-body>
        <b-card-img src="/static/blank_box.jpg" style="height: 12rem"/>
        <b-card-body>
          <b-skeleton width="50%"/>
          <b-skeleton class="mt-3" width="30%"/>
          <b-skeleton class="mt-2" width="30%"/>
        </b-card-body>
      </b-card>
    </template>


    <b-card no-body>
      <div class="position-relative">
        <b-card-img-lazy
            :src="game.game.image"
            class="img-cover"
            blank-src="/static/blank_box.jpg"
            blank-height="10rem"
            style="height: 10rem; border-bottom-left-radius: 0; border-bottom-right-radius: 0"
        />
        <div v-if="isAdmin()" class="position-absolute" style="top:0; right: 0;">

          <b-dropdown size="lg" right variant="link" toggle-class="text-decoration-none" no-caret>
            <template #button-content>
              <b-icon-three-dots-vertical class="text-white mr-n3"
                                          style="filter: drop-shadow( 1px 1px 3px rgba(0, 0, 0, 1));" font-scale="2"/>
            </template>
            <b-dropdown-item v-b-modal="`modal-${game.id}`">Update stock</b-dropdown-item>
            <b-dropdown-item @click="deleteGame(game.id)">Delete</b-dropdown-item>
          </b-dropdown>
        </div>
      </div>

      <b-card-body>
        <span class="text-nowrap overflow-hidden d-block">
          {{ game.game.name }}
        </span>

        <b-row class="mt-3">
          <b-col>
            <div v-if="isAdmin()" >
              <span class="text-muted">Stock: </span><span class="text-muted font-weight-bold">{{game.stock}}</span>
            </div>
            <div v-else>
          <span v-if="game.is_available" class="small text-success d-block">
            Available
          </span>
          <span v-if="!game.is_available" class="small d-block text-danger"
          >Sold out</span>
              </div>
            </b-col>
          <b-col cols="auto">
            <div class="">
              <h3 class="text-gray-900 mb-0" style="font-weight: 400">
                {{ game.selling_price }} €
              </h3>
            </div>
          </b-col>
        </b-row>
      </b-card-body>

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
    </b-card>
  </b-skeleton-wrapper>
</template>

<script>
import gamesMixin from '@/mixins/games.mixin'
import usersMixin from '@/mixins/users.mixin'
import storeService from '@/services/store.service'

export default {
  name: 'StoreHomePartialGameCard',
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
    deleteGame(game_id){
      storeService.deleteGame(game_id).then(() => {
        this.$emit('delete', game_id)
      })
    }
  }
}
</script>

<style scoped></style>
