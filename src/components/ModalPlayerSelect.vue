<template>
  <!-- Modal -->

  <ModalSelect
      :id="id"
      :items="players"
      :title="title"
      item-metadata="email"
      item-title="name"
      @search="search"
      @selected="$emit('player-selected', $event)"
  >
    <template v-if="isNewPlayer" v-slot:header>
      <div class="d-flex flex-row align-items-center justify-content-between flex-fill">
        <div class="d-flex flex-fill mr-auto">
          <b-button v-show="isNewPlayer" size="sm" variant="info" @click="isNewPlayer=false">
            Search for players
          </b-button>
        </div>
        <div class="d-flex flex-fill justify-content-center">
          <h4 v-show="isNewPlayer" class="mb-0">Add player</h4>
        </div>
        <div class="d-flex flex-fill ml-auto"></div>
      </div>
    </template>

    <template v-if="isNewPlayer" #content>
      <div>

        <form>
          <div class="px-4 mt-4">
            <b-alert show variant="warning">E-mail already registered</b-alert>
            <b-form-group invalid-feedback="This field is required" label="Name">
              <b-form-input
                  v-model="form.name"
                  :state="validateState('name')"
                  placeholder="Full name"
                  type="text"/>
            </b-form-group>

            <b-form-group invalid-feedback="Please insert a valid e-mail address" label="E-mail">
              <b-form-input
                  v-model="form.email"
                  :state="validateState('email')"
                  placeholder="eg. name@mail.com"
                  type="text"/>
            </b-form-group>

          </div>
        </form>
      </div>

    </template>
    <template #footer>
      <button v-if="!isNewPlayer" class="btn btn-info" type="button" @click="doNewPlayer">
        New player
      </button>
      <b-button
          v-if="isNewPlayer"
          variant="primary"
          @click="onSubmit">
        <span v-show="!loading">Add</span>
        <b-spinner v-show="loading" small/>
      </b-button>
    </template>
  </ModalSelect>

</template>

<script>
import usersMixin from '@/mixins/users.mixin'
import formMixin from '@/mixins/form.mixins'
import playerService from '@/services/player.service'
import ModalSelect from "@/components/ModalSelect";

import {email, required} from 'vuelidate/lib/validators'

export default {
  name: "ModalPlayerSelect",
  mixins: [usersMixin, formMixin],
  props: ['id', 'title'],
  components: {ModalSelect},
  data: function () {
    return {
      isNewPlayer: false,
      selectedPlayer: undefined,
      players: [],
      form: {
        name: '',
        email: ''
      },
      loading: false
    }
  },
  methods: {
    doNewPlayer(e) {
      e.preventDefault();
      this.isNewPlayer = true;
    },
    search(val) {
      playerService.searchPlayers(val).then(response => this.players = response)
    },
    onSubmit() {
      this.$v.form.$touch();
      if (this.$v.form.$anyError) {
        return;
      } else {
        this.loading = true;
        playerService.createPlayer(this.form).then((response) => {
          this.loading = false
          this.$bvModal.hide(this.id)
          this.$emit('player-selected', response)
        })

      }
    }
  },
  validations: {
    form: {
      name: {
        required
      },
      email: {
        email, required
      }
    }
  }
}
</script>

<style scoped>

</style>