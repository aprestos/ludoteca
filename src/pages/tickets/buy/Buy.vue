<template>
<Wizard
    :title="currentStep.title"
    :description="currentStep.description"
    :current-step="currentStepNumber"
    :number-of-steps="3"
    :loading="loading"
    @next="nextStep"
    @previous="previousStep"
    @finish="finish"
>
  <template #content>
    <div v-if="currentStepNumber === 1">
      <Step1 :ticket="$route.params.ticket"></Step1>
    </div>
    <div v-if="currentStepNumber === 2">
      <Step2 :value="names" @input="onStep2Input"></Step2>
    </div>
    <div v-if="currentStepNumber === 3">
      <Step3 :tickets="[buyer_ticket].concat(additional_tickets)"></Step3>
    </div>
  </template>
</Wizard>
</template>

<script>
import Wizard from "@/pages/templates/Wizard.vue"
import Step1 from "@/pages/tickets/buy/partials/Step1.vue"
import Step2 from "@/pages/tickets/buy/partials/Step2.vue"
import Step3 from "@/pages/tickets/buy/partials/Step3.vue"
import ticketService from "@/services/ticket.service"
import orderService from "@/services/order.service"
import ticketsMixin from "@/mixins/tickets.mixin"

let steps = {
  1: {title: "Let's start", description: "Your ticket is already here for you"},
  2: {title: "Additional tickets", description: "Bring some friends to play, drink or get together"},
  3: {title: "Summary", description: "Last step! We promise 🙏"}
}


export default {
  name: "Buy",
  components: {Step3, Step2, Step1, Wizard },
  mixins: [ticketsMixin],
  props: ['ticket'],
  data(){
    return {
      currentStepNumber: 1,
      currentStep: steps[1],
      buyer_ticket: {},
      additional_tickets: [],
      tickets: [],
      names: [""],
      loading: false
    }
  },
  mounted() {
    ticketService.fetchTickets().then((data)=> this.tickets = data)
  },
  methods: {
    nextStep(){
      if(this.currentStepNumber === 1){
        this.buyer_ticket = {
          name: this.$store.getters["users/current"].name,
          ticket: this.$route.params.ticket
        }
      } else if(this.currentStepNumber === 2) {
        this.additional_tickets = []
        const ticket_info = this.getValidTickets(this.tickets).filter(ticket => ticket.type === "standard")[0]
        this.names.filter(Boolean).forEach((name) => this.additional_tickets.push({
          name: name,
          ticket: ticket_info,
        }))
      }

      this.currentStep = steps[++this.currentStepNumber]

    },
    previousStep(){
      this.currentStep = steps[--this.currentStepNumber]
    },
    finish(){
      this.loading = true
      const products = [this.buyer_ticket].concat(this.additional_tickets)

      orderService.createOrder(
          this.$store.getters["users/current"],
          products,
      ).then(() => {
        this.$toast.success("Done. Check your inbox for payment details")
        this.$router.push({name: "Home"})
      }).finally(()=> {
        this.loading = false
      })
    },
    onStep2Input(names){
      this.names = names
    }
  }
}
</script>

<style scoped>

</style>
