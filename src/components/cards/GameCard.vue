<template>
  <div class="mb-6 w-100">

    <b-skeleton-wrapper :loading="loading">
      <template #loading>
        <b-skeleton-img width="100%" style="aspect-ratio: 1"/>
          <div class="d-flex flex-column">
            <span class="mt-3">
              <b-skeleton width="50%" />
            </span>
            <slot name="loading"></slot>
          </div>
      </template>
      <div
        class="
          image-zoom
          position-relative
          d-block
          overflow-hidden
          shadow
          rounded
        "
        style="width: 100%; height: 0; padding-bottom: 100%"
      >
        <b-link v-b-modal="`details-game-${game_id}`">
          <progressive-img
              class="rounded"
              :src="game.thumbnail"
              :src-fallback="game.thumbnail"
              :aspect-ratio="1"
          />
          <div
            class="
              overlay
              d-none
              align-items-end
              justify-content-end
              p-3
              position-absolute
              text-white
              h-100
              w-100
            "
          >
            <b-icon-zoom-in font-scale="2" />
          </div>
        </b-link>
      </div>

      <div class="d-flex flex-column">
        <span
          class="mt-3 mb-0 font-condensed"
          style="
            font-size: 1.125rem;
            font-weight: 400;
            letter-spacing: 0.02rem;
            display: -webkit-box;
            -webkit-line-clamp: 1;
            -webkit-box-orient: vertical;
            overflow: hidden;
          "
        >
          {{ game.name }}
        </span>
        <slot name="content"></slot>
      </div>
    </b-skeleton-wrapper>
    <b-modal
      hide-footer
      header-class="p-0"
      :id="`details-game-${game_id}`"
    >
      <template #modal-header>
        <div class="position-relative">
          <div class="position-absolute p-3 top w-100 right">
          <b-button
            size="lg"
            @click="hideModal"
            variant="dark"
            class="btn-rounded-circle shadow lift"
            style="opacity: 90%"
          >
            <b-icon-x
          /></b-button>
        </div>
          <b-card-img :src="game.image" />
        </div>
      </template>
      <template #default>
        <b-row>
          <b-col>
            <b-media vertical-align="center">
              <template #aside>
                <b-icon-people-fill scale="2"/>
              </template>
              <span class="text-muted text-uppercase small font-weight-bold">Players</span><br/>
              <span>{{ range(game.min_players, game.max_players) }}</span>
            </b-media>
          </b-col>
          <b-col>
            <b-media vertical-align="center">
              <template #aside>
                <b-icon-clock-fill scale="2"/>
              </template>
              <span class="text-muted text-uppercase small font-weight-bold">Playtime</span><br/>
              <span>{{ range(game.min_playtime, game.max_playtime) }}</span>
            </b-media>
          </b-col>
        </b-row>
      </template>
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
      type: Number,
    },
    imageHeight: {
      default: '8rem',
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
    game: {
      type: Object
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
      },
    },
  },
  mixins: [gamesMixin],
  methods: {
    hideModal() {
      this.$bvModal.hide(`details-game-${this.game_id}`)
    },
  },
}
</script>

<style lang="scss">
.overlay {
  background-color: rgba(0, 0, 0, 0.5);
}

.image-zoom:hover {
  .overlay {
    display: flex !important;
  }
}

.progressive-image-main{
  object-fit: cover;
  height: 100% !important;
}
</style>
