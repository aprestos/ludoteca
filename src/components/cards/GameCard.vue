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
      <div class="position-relative d-block overflow-hidden rounded shadow"
           style="width:100%; height: 0; padding-bottom: 100%">
        <b-img-lazy
            :src="image"
            blank-src="/static/blank_box.jpg"
            class="w-100 h-100 position-absolute opaci"
            style="top:0; left: 0; object-fit: cover"
        />
      </div>

      <div class="d-flex flex-column">
      <span class="mt-3"
            style="display: -webkit-box; -webkit-line-clamp:1;-webkit-box-orient: vertical; overflow: hidden; ">
          {{ title }}
        </span>
        <slot name="content"></slot>
      </div>

    </b-skeleton-wrapper>
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
}
</script>

<style scoped>
</style>
