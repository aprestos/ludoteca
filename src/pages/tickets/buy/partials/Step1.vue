<template>
  <b-card>
    <div class="d-flex column align-items-center w-100">
      <div>
         <i v-if="(isAssociate() || isStaff()) && ticket.type === 'membership'" style="font-size: 3rem;" class="bi-ticket-detailed-fill text-info" role="img" aria-label="Ticket"/>
         <i v-else style="font-size: 3rem;" class="bi-ticket-detailed-fill text-dark" role="img" aria-label="Ticket"/>
      </div>
      <div class="ml-3 flex-1">
          <p class="font-size-lg mb-0">{{$store.getters["users/current"].name }}</p>
          <p class="text-muted mb-0">{{ticket.name}}</p>
      </div>
      <span class="ml-auto" style="font-size: 2rem; font-weight: 200">
          {{formatPrice(ticket.price)}}€
      </span>
    </div>
  </b-card>
</template>

<script>
import usersMixin from "@/mixins/users.mixin"
import {formatPrice} from "@/utils/number.utils"

export default {
  name: "step1",
  methods: {formatPrice},
  mixins: [usersMixin],
  props: ['ticket'],
}
</script>

<style scoped>

</style>
