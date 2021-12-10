<template>
  <HomeScreenTemplate pre-title="LEIRIACON 2022" title="Dashboard">

    <b-row>
      <b-col sm="6" xl="4">
        <NumbersCard icon="box-seam" title="Games" :value="content.library.games.total">
          <template #metadata>
          <NumbersMetadata :loading="loading" icon="person-square" :value="content.library.games.being_played"/>
            <NumbersMetadata class="ml-6" :loading="loading" icon="x-circle" :value="content.library.games.not_checked_in"/>
            </template>
        </NumbersCard>
      </b-col>
      <b-col sm="6" xl="4">
        <NumbersCard icon="person-check" :loading="loading" title="Players" :value="content.library.requisitors.total">
          <template #metadata>
          <NumbersMetadata :loading="loading" icon="people" :value="`${content.library.withdraws.players.min_players} - ${content.library.withdraws.players.max_players}`"/>
            </template>
        </NumbersCard>
      </b-col>
      <b-col sm="6" xl="4">
        <NumbersCard icon="box-arrow-up" :loading="loading" title="Withdraws" :value="content.library.withdraws.total">
          <template #metadata>
          <NumbersMetadata :loading="loading" icon="clock" :value="adaptDuration(content.library.withdraws.duration.average)"/>
            </template>
        </NumbersCard>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12" md="6">

        <b-card title="Popular games" no-body>
          <b-card-header><h4 class="card-header-title">Popular games</h4></b-card-header>
          <b-skeleton-wrapper :loading="loading">
            <template #loading>
              <b-skeleton-table :table-props="{ small: true}" :rows="5"/>
            </template>
            <b-table small :fields="['game','requisitions']" :items="content.library.withdraws.popular.games"/>
          </b-skeleton-wrapper>
        </b-card>

      </b-col>
      <b-col cols="12" md="6">
        <b-card no-body>
          <b-card-header>
            <h4 class="card-header-title">Frequent requisitors</h4></b-card-header>
          <b-skeleton-wrapper :loading="loading">
            <template #loading>
              <b-skeleton-table :table-props="{ small: true}" :rows="5"/>
            </template>
            <b-table small :fields="['name', 'count']" :items="content.library.withdraws.popular.requisitors"/>
          </b-skeleton-wrapper>
        </b-card>
      </b-col>
    </b-row>
    <span class="text-uppercase text-muted small mb-3">Latest returns</span>
    <DashboardWithdraws :loading="loading" class="mt-3" :withdraws="content.library.withdraws.recent.in"/>
    <span class="text-uppercase text-muted small mb-3">Latest withdraws</span>
    <DashboardWithdraws :loading="loading" class="mt-3" :withdraws="content.library.withdraws.recent.out"/>
  </HomeScreenTemplate>
</template>

<script>
import HomeScreenTemplate from "@/components/templates/HomeScreenTemplate"
import dashboardService from "@/services/dashboard.service"
import DashboardWithdraws from './partials/Withdraws'
import NumbersCard from "@/pages/dashboard/partials/NumbersCard"
import NumbersMetadata from "@/pages/dashboard/partials/NumbersMetadata"

export default {
  name: "home",
  components: {
    NumbersMetadata,
    NumbersCard,
    HomeScreenTemplate,
    DashboardWithdraws,
  },
  data() {
    return {
      content: {
        library: {
          games: {
            total: 0,
            being_played: 0,
            not_checked_in: 0
          },
          requisitors: {
            total: 0
          },
          withdraws: {
            total: 59,
            recent: {
              out: [],
              in: []
            },
            popular: {
              requisitors: [],
              games: []
            },
            players: {
              min_players: 0,
              max_players: 0
            },
            duration: {
              average: 0
            }
          }
        },
      },
      loading: true
    }
  },
  mounted() {
    dashboardService.getContent().then(response => {
      this.content = response
      this.loading = false
    })
  },
  methods: {
    adaptDuration(duration) {

      const sec_num = parseInt(duration, 10) // don't forget the second param
      const hours = Math.floor(sec_num / 3600)
      const minutes = Math.floor((sec_num - (hours * 3600)) / 60)

      return hours + ':' + minutes
    }
  }
}
</script>

<style scoped>

</style>