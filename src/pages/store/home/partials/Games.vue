<template>
  <div>
    <b-row >
      <b-col v-for="(game, index) in games" :key="index" cols="6" sm="4" md="3" xl="2">
        <Game :game="game" :loading="loading" @update="$emit('update', $event)" @delete="$emit('delete', $event)"/>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import Game from './Game'


export default {
  name: 'Games',
  components: {
    Game,
  },
  props: {
    games: {
      type: Array,
      required: true,
    },
    loading: {
      type: Boolean,
      default: true,
    },
  },
}
</script>

<style scoped></style>
