<template>
<div class="main-content">

  <!-- HEADER -->
  <div class="pt-3 pb-8 bg-hero bg-ellipses">
    <div class="container-fluid">
      <div class="mb-5 ml-5">

      </div>
      <div class="row justify-content-center">
        <div class="col-md-10 col-lg-8 col-xl-6">

          <div class="mb-5 d-flex row justify-content-center">

            <b-link :to="{'name': 'Home'}">
              <b-icon-house-fill/> Home
            </b-link>
          </div>
          <div class="mb-5 d-flex row justify-content-center">

            <b-link :to="{'name': 'Home'}">
              <img width="300rem" src="@/assets/whitelogo.png"/>
            </b-link>
          </div>
          <!-- Text -->
          <p class="lead text-center text-muted">
            Be part of LeiriaCON. Get your ticket, get all the fun.
          </p>
        </div>
      </div> <!-- / .row -->
    </div>
  </div>

  <!-- CONTENT -->
  <div class="container">
    <div class="row mt-n7 justify-content-center" v-show="!loading">
      <div class="col-12 col-lg-6" v-for="(type_tickets, index) in Object.values(tickets)" v-bind:key="index">
        <!-- Card -->
        <div class="card" v-for="(ticket, index) in getValidTickets(type_tickets)" v-bind:key="index">
        <div class="card-body">

          <!-- Title -->
          <h6 class="text-uppercase text-center text-muted my-4">
            {{ ticket.name }}
          </h6>

          <!-- Price -->
          <div class="row g-0 align-items-center justify-content-center">
            <div class="col-auto">
              <div class="h2 mb-0">€</div>
            </div>
            <div class="col-auto">
              <div class="display-2 mb-0">{{ formatPrice(ticket.price) }}</div>
            </div>
            <div class="d-flex align-self-start justify-content-start" v-if="getHigherPrice(type_tickets)>ticket.price">
              <s class="align-self-start h1 text-muted mt-1">{{ formatPrice(getHigherPrice(type_tickets)) }}</s>
            </div>
          </div> <!-- / .row -->

          <!-- Period -->
          <div class="h6 text-uppercase text-center text-muted mb-5">
            / person 12+ years old
          </div>

          <!-- Features -->
          <div class="mb-3">
            <ul class="list-group list-group-flush">
              <li
                  v-for="(perk, index) in ticket.perks"
                  class="list-group-item d-flex align-items-center justify-content-between px-0"
                  v-bind:key="index"
              >
                <div>
                  <small>{{ perk.text }}</small>
                  <b-link v-if="perk.tooltip" v-b-tooltip:hover class="ml-2 text-info" title="Only for buyer">
                    <b-icon-info-circle-fill/>
                  </b-link>
                </div>
                <i v-if="perk.value==='true'" class="fe fe-check-circle text-success"></i>
                <small v-else>{{ perk.value }}</small>
              </li>
            </ul>
          </div>

          <b-button v-if="new Date(ticket.validFrom) > new Date() && !isStaff()" variant="light" block disabled>
            Coming December 5th
          </b-button>
          <!-- TODO Change this! -->
          <b-button v-if="true" variant="light" block disabled>
            Sold out
          </b-button>
          <b-button v-else-if="!isAuthenticated()" :to="{name: 'Login'}" variant="primary" block>
            Login
          </b-button>
          <b-alert v-else-if="ticket.type === 'membership' && !isAssociate() && !isStaff()" show variant="light"><b-icon-award-fill/> Member exclusive. See how to become one <b-link target="_blank" href="https://www.spielportugal.org/membership">here</b-link></b-alert>
          <b-alert v-else-if="hasPreviousOrders && !isStaff()" show variant="warning"><b-icon-exclamation-circle-fill/> Only one purchase per account is allowed</b-alert>
          <b-button v-else :to="{name: 'BuyTickets', params: { 'ticket': ticket } }" variant="primary"  block>
            Buy
          </b-button>
        </div>
      </div>
      </div>
    </div> <!-- / .row -->
    <div class="row justify-content-center">
      <div class="col-12 col-lg-6">

        <!-- Card -->
        <div class="card card-inactive">

          <div class="card-body">

            <!-- Title -->
            <h3 class="text-center">
              Need some help deciding?
            </h3>

            <!-- Text -->
            <p class="text-muted text-center">
              We can help you if you have any questions about our tickets or about the event.
            </p>
                <!-- Button -->
                <div class="text-center">
                  <a href="mailto:info@spielportugal.org" class="btn btn-outline-secondary">
                    Contact us
                  </a>
                </div>
          </div>
        </div>

      </div>
      <div class="col-12 col-lg-6">

        <!-- Card -->
        <div class="card card-inactive">
          <div class="card-body">

            <!-- Title -->
            <h3 class="text-center">
              Want to become a Member?
            </h3>

            <!-- Text -->
            <p class="text-muted text-center">
              You can become an Member now, check all the benefits using the link below.
            </p>

            <!-- Button -->
            <div class="text-center">

              <b-button href="https://www.spielportugal.org/membership" target="_blank" class="btn" variant="outline-secondary">
                See more
              </b-button>
            </div>
          </div>
        </div>

      </div>
    </div> <!-- / .row -->
    <Modal/>
  </div>
<b-modal>

</b-modal>
</div>
</template>

<script>
import Modal from "./partials/Modal.vue"
import usersMixin from "@/mixins/users.mixin"
import orderService from "@/services/order.service"
import ticketService from "@/services/ticket.service"
import {formatPrice} from "@/utils/number.utils"
import ticketsMixin from "@/mixins/tickets.mixin"

export default {
  name: "Buy",
  methods: {
    formatPrice: formatPrice,
    getHigherPrice(tickets){
      let higherPrice = 0
      tickets.forEach((ticket) => {
        if(ticket.price && ticket.price > higherPrice){
          higherPrice = ticket.price
        }
      })
      return higherPrice
    }
  },
  components: {Modal},
  mixins: [usersMixin, ticketsMixin],
  data(){
    return {
      hasPreviousOrders: false,
      tickets: {},
      loading: true,
      edition: {}
    }
  },
  created() {
    ticketService.fetchTickets().then((response) => {
      response.forEach((ticket) => {
        console.log(ticket.validUntil)
        if(!this.tickets[ticket.type]?.length){
          this.tickets[ticket.type] = []
        }

        this.tickets[ticket.type].push(ticket)
      })
    }).finally(()=> this.loading = false)

    if(this.isAuthenticated()){
      orderService.getOrders({'user__id': this.$store.getters["users/current"].id}).then((response) => {
        if (response.length > 0) this.hasPreviousOrders = true
      })
    }
  },
}
</script>

<style scoped>

</style>
