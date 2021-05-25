<template>
  <!-- Modal -->
  <ModalSelect
      :id="id"
      :hide-footer="true"
      :items="games"
      :title="title"
      :loading="loading"
      item-metadata="year"
      item-title="name"
      @search="search"
      @selected="$emit('game-selected', $event)"
  >
  </ModalSelect>
</template>

<script>
import bggService from '@/services/bgg.service'
import ModalSelect from '@/components/ModalSelect'

export default {
  name: 'ModalGameSelect',
  props: ['id', 'title'],
  components: {
    ModalSelect,
  },
  data: function () {
    return {
      games: [],
      loading: false,
    }
  },
  methods: {
    search(val) {
      this.loading = true
      Promise.all([
        bggService.search(val),
        new Promise(r => setTimeout(r, 750))
      ]).then((responses)=>this.games = responses[0]).finally(() => this.loading = false)
    },
  },
}
</script>

<style scoped></style>
