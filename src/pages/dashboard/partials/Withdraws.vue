<template>
  <b-row>
    <b-col v-for="(withdraw, index) in withdraws" :key="index">
      <l-game-card :loading="loading" :image="withdraw.image" :game_id="withdraw.game_id" :title="withdraw.game">
        <template #loading>
          <b-skeleton width="100%"/>
        </template>
        <template #content>
          <time-ago class="text-muted small" :datetime="withdraw.date" long tooltip/>
        </template>
      </l-game-card>
    </b-col>
    </b-row>
</template>

<script>
import LGameCard from "@/components/cards/GameCard"
import { TimeAgo } from 'vue2-timeago'

export default {
  name: "DashboardWithdraws",
  components: {LGameCard, TimeAgo},
  props: {
    withdraws: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>

</style>