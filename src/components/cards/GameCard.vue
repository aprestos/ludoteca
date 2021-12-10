<template>
  <div class="mb-6 w-100">
    <b-skeleton-wrapper :loading="loading">
      <template #loading>
        <div class="position-relative">
          <div class="position-relative d-block overflow-hidden rounded shadow"
               style="width:100%; height: 0; padding-bottom: 100%">
            <b-img
                class="w-100 h-100 position-absolute"
                src="/static/blank_box.jpg"
                style="top:0; left: 0; object-fit: cover"
            />
          </div>


          <div class="d-flex flex-column">
          <span class="mt-3">
            <b-skeleton width="50%"/>
          </span>
            <slot name="loading"></slot>
          </div>
        </div>

      </template>
      <div class="image-zoom position-relative d-block overflow-hidden rounded shadow"
           style="width:100%; height: 0; padding-bottom: 100%">
        <b-link v-b-modal="`details-game-${game_id}`">
        <b-img-lazy
            :src="image"
            blank-src="/static/blank_box.jpg"
            class="w-100 h-100 position-absolute"
            style="top:0; left: 0; object-fit: cover"
        />
          <div class="overlay d-none align-items-end justify-content-end p-3 position-absolute text-white h-100 w-100">
          <b-icon-zoom-in font-scale="2"/>
            </div>
          </b-link>

      </div>

      <div class="d-flex flex-column">
      <span class="mt-3"
            style="display: -webkit-box; -webkit-line-clamp:1;-webkit-box-orient: vertical; overflow: hidden; ">
          {{ title }}
        </span>
        <slot name="content"></slot>
      </div>

    </b-skeleton-wrapper>
    <b-modal body-class="p-0" hide-header hide-footer :id="`details-game-${game_id}`">
      <div class="position-relative">
        <div class="position-absolute p-3 top w-100 right ">
          <b-button size="lg" @click="hideModal" variant="dark" class="btn-rounded-circle shadow lift" style="opacity: 90%">
            <b-icon-x/></b-button>
        </div>
      <b-card-img :src="image"/>
        </div>
    </b-modal>
  </div>
</template>


<script>
import gamesMixin from '@/mixins/games.mixin'

export default {
  name: 'LGameCard',
  props: {
    loading: {
      default: false,
      type: Boolean,
    },
    game_id: {
      required: true,
      type: Number
    },
    title: {
      default: '',
      type: String,
    },
    image: {
      default: '',
      type: String,
    },
    imageHeight: {
      default: '8rem',
      type: String
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
      type: Boolean
    },
    selected: {
      default: false,
      type: Boolean
    }
  },
  computed: {
    gameSelected: {
      get() {
        return this.selected
      },
      // eslint-disable-next-line no-unused-vars
      set(val) {
        this.$emit('selected-change', this.game_id)
      }
    }
  },
  mixins: [gamesMixin],
  methods: {
    hideModal() {
        this.$bvModal.hide(`details-game-${this.game_id}`)
      },
  }
}
</script>

<style scoped lang="scss">
.overlay {
  background-color: rgba(0, 0, 0, 0.5)
}

.image-zoom:hover {
  .overlay {
    display: flex !important;
  }
}
</style>
