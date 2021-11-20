<template>
  <HomeScreenTemplate :title="title" :pre-title="pretitle">
    <template #actions>

      <b-alert class="mb-0 d-inline-block" v-if="!isAdmin()" variant="warning" :show="true"><b-icon-patch-exclamation-fill/> 10% discount for Associates</b-alert>

      <b-button class="d-inline-block" v-if="isAdmin()" variant="primary" :to="{name: 'StoreAddGame'}">Add game</b-button>
    </template>
    <Games :loading="loading" :games="games" @update="updateGame" @delete="deleteGame"/>

  </HomeScreenTemplate>
</template>

<script>
import Games from "@/pages/store/home/partials/Games"
import HomeScreenTemplate from "@/components/templates/HomeScreenTemplate"
import storeService from "@/services/store.service"
import usersMixin from "@/mixins/users.mixin"

export default {
  name: 'StoreHome',
  components: {
    HomeScreenTemplate,
    Games,
  },
  mixins: [usersMixin],
  props: ['title', 'pretitle'],
  data() {
    return {
      games: [],
      loading: true
    }
  },
  mounted(){
    storeService.fetchGames(1).then(response => {
      this.games = response.results
      this.loading = false
    })
  },
  computed:{
    associate_discount(){
      const configurations = this.$store.getters['configurations/all']
      if (configurations){
        return configurations.filter(conf => conf.key === 'associate_discount')[0].value
      }
      return 1
    }
  },
  methods: {
    updateGame(game){
      if (game) {
        const outdatedGameObject = this.games.filter((item) => item.id === game.id)[0]
        this.$set(this.games, this.games.indexOf(outdatedGameObject), game)
      } else {
        storeService.fetchGames().then(response => this.games = response)
      }
    },
    deleteGame(game_id){
      if (game_id){
        const outdatedGameObject = this.games.filter((item) => item.id === game_id)[0]
        this.games.splice(this.games.indexOf(outdatedGameObject), 1)
      } else {
        storeService.fetchGames().then(response => this.games = response)
      }
    }
  }
}
</script>

<style scoped></style>
