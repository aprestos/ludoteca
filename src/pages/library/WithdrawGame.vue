<template>
  <WizardScreen :title="game.game.name"
                :back-to="{ name: 'LibraryHome' }"
                pre-title="Withdraw"
                @submit="doWithdraw">
    <template #content>
      <b-form>
        <b-form-group
            label="Requisitor" invalid-feedback="Required">
          <l-form-select
            v-model="requisitor.name"
            :state="validateState('requisitor_id')"
            @select="$bvModal.show('player-select')"/>
        </b-form-group>

      <b-alert v-if="game.notes" variant="dark" show>
        <b-icon-info-circle-fill class="mr-3" />
      {{game.notes}}
      </b-alert>
        <ModalPlayerSelect
          id="player-select"
          title="Players"
          v-on:player-selected="setRequisitor"
        >
        </ModalPlayerSelect>

        <b-form-group class="mt-5" label="Location">
          <LocationShelves :location="game.location" />
        </b-form-group>

      </b-form>
    </template>
  </WizardScreen>
</template>

<script>
import usersMixin from '@/mixins/users.mixin'
import gamesMixin from '@/mixins/games.mixin'
import axiosMixin from '@/mixins/axios.mixin'
import withdrawService from '@/services/withdraw.service'
import libraryService from '@/services/library.service'
import ModalPlayerSelect from '@/components/ModalPlayerSelect'
import WizardScreen from '@/components/templates/InputScreenTemplate'
import LocationShelves from '@/components/location/LocationShelves'
import LFormSelect from "@/components/form/LFormSelect"

import formMixin from '@/mixins/form.mixins'

import { required } from 'vuelidate/lib/validators'

export default {
  name: 'WithdrawGame',
  components: {
    LocationShelves,
    ModalPlayerSelect,
    WizardScreen,
    LFormSelect
  },
  mixins: [usersMixin, axiosMixin, gamesMixin, formMixin],
  props: ['title', 'pretitle'],
  data() {
    return {
      game: {
        game: {
          name: '',
        },
        location: '',
      },
      requisitor: {},
      form: {
        requisitor_id: '',
      },
    }
  },
  methods: {
    doWithdraw() {

      this.$v.form.$touch()
      if (this.$v.form.$anyError) {
        return
      }

      let data = {
        requisitor_id: this.form.requisitor_id,
        game_id: this.game.id,
      }

      withdrawService
        .withdrawGame(data)
        .then(() => {
          this.$toast.success(
            'Success! Don\'t forget to give the game to '+ this.requisitor.name,
          )
          this.$router.push({ name: 'Home' })
        })
        .catch((response) => this.$toast(this.getErrorDescription(response)))
    },
    setRequisitor(player) {
      this.requisitor = player
      this.form.requisitor_id = player.id
      this.$bvModal.hide('player-select')
    },
  },
  mounted() {
    libraryService
      .fetchGame(this.$route.params.id)
      .then((response) => (this.game = response))
  },
  validations: {
    form: {
      requisitor_id: {
          required,
      },
    },
  },
}
</script>

<style scoped></style>
