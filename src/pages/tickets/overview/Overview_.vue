<template>
<div class="main-content">

  <!-- HEADER -->
  <div class="pt-3 pb-8 bg-dark bg-ellipses">
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

  {{tickets}}
  <!-- CONTENT -->
  <div class="container">
    <div class="row mt-n7 justify-content-center" v-show="!loading">
      <div class="col-12 col-lg-6" v-for="(ticket, index) in tickets" v-bind:key="index">

        <!-- Card -->
        <div class="card">
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
                <div class="display-2 mb-0">5</div>
              </div>
              <div class="d-flex align-self-start justify-content-start">
                <s class="align-self-start h1 text-muted mt-1">10</s>
              </div>
            </div> <!-- / .row -->

            <!-- Period -->
            <div class="h6 text-uppercase text-center text-muted mb-5">
              / person 12+ years old
            </div>

            <!-- Features -->
            <div class="mb-3">
              <ul class="list-group list-group-flush">
                <li class="list-group-item d-flex align-items-center justify-content-between px-0">
                  <div>
                    <small>Personalized Badge</small>
                    <b-link v-b-tooltip:hover class="ml-2 text-info" title="Only for buyer"><b-icon-info-circle-fill/></b-link>
                  </div>
                  <i class="fe fe-check-circle text-success"></i>
                </li>
                <li class="list-group-item d-flex align-items-center justify-content-between px-0">
                  <small>Full access</small> <i class="fe fe-check-circle text-success"></i>
                </li>
                <li class="list-group-item d-flex align-items-center justify-content-between px-0">
                  <small>4-days</small> <i class="fe fe-check-circle text-success"></i>
                </li>
                <li class="list-group-item d-flex align-items-center justify-content-between px-0">
                  <small>Additional tickets</small> <small>3</small>
                </li>
              </ul>
            </div>

            <!-- Button -->
<!--            <b-button v-if="tickets.length===0" variant="light" block disabled>-->
<!--              Coming soon-->
<!--            </b-button>-->
<!--            <b-button v-else-if="!isAuthenticated()" :to="{name: 'Login'}" variant="primary" block>-->
<!--              Login-->
<!--            </b-button>-->
<!--            <b-alert v-else-if="!isAssociate() && !isStaff()" show variant="light"><b-icon-award-fill/> Member exclusive. See how to become one <b-link target="_blank" href="https://www.spielportugal.org/membership">here</b-link></b-alert>-->
<!--            <b-alert v-else-if="this.hasPreviousOrders && !isStaff()" show variant="warning"><b-icon-exclamation-circle-fill/> One purchase per Member</b-alert>-->
<!--            <b-button v-else :to="{name: 'BuyTickets'}" variant="primary" block>-->
<!--              Buy-->
<!--            </b-button>-->
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

export default {
  name: "Overview_",
  components: {Modal},
  mixins: [usersMixin],
  data(){
    return {
      hasPreviousOrders: false,
      tickets: [],
      loading: true
    }
  },
  mounted() {
    ticketService.fetchTickets().then((response)=> {
      this.tickets = response
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
