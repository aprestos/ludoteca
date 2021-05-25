<template>
  <WizardScreen
    :back-to="{ name: 'Home' }"
    pre-title="library"
    title="New game"
    @submit="onSubmit"
  >
    <template #content>

        <!-- Game -->
        <b-form-group class="max-width-3-md" invalid-feedback="This field is required" label="Game">

          <l-form-select
            v-model="game.name"
            :state="validateState('game_id')"
            @select="$bvModal.show('game-select-modal')"/>

          <!-- modal -->
          <ModalGameSelect
            id="game-select-modal"
            @game-selected="assignGame"
          ></ModalGameSelect>
        </b-form-group>

        <!-- Owner -->
        <b-form-group class="max-width-3-md" invalid-feedback="This field is required" label="Owner">
          <l-form-select
            v-model="player.name"
            :state="validateState('owner_id')"
            @select="$bvModal.show('player-select-modal')"/>

          <!-- Owner modal -->
          <ModalPlayerSelect
            id="player-select-modal"
            @player-selected="assignPlayer"
          ></ModalPlayerSelect>
        </b-form-group>

        <!-- Location -->
        <b-form-group
            class="max-width-2-md"
          invalid-feedback="This field is required"
          label="Location"
        >
          <b-form-input
            v-model="form.location"
            :state="validateState('location')"
            hidden
          />
          <FormSelect
            v-model="form.location"
            :options="$store.getters['library/locations']"
            :state="validateState('location')"
            option-text="name"
            option-value="id"
          />
        </b-form-group>

        <!-- Notes -->
        <b-form-group description="Optional" label="Notes">
          <b-form-textarea
              size="lg"
            v-model="form.notes"
            placeholder="Eg. expansion included, missing components"
          ></b-form-textarea>
        </b-form-group>

        <div class="d-flex flex-row justify-content-end mt-5">
        </div>
    </template>
  </WizardScreen>
</template>

<script>
import ModalGameSelect from '@/components/ModalGameSelect'
import bggService from '@/services/bgg.service'
import libraryService from '@/services/library.service'
import gamesMixin from '@/mixins/games.mixin'
import formMixin from '@/mixins/form.mixins'
import ModalPlayerSelect from '@/components/ModalPlayerSelect'
import InputScreenTemplate from '@/components/templates/InputScreenTemplate'
import FormSelect from '@/components/FormSelect'
import LFormSelect from "@/components/form/LFormSelect"

import { required } from 'vuelidate/lib/validators'

export default {
  name: 'AddGame',
  components: {
    WizardScreen: InputScreenTemplate,
    ModalPlayerSelect,
    ModalGameSelect,
    FormSelect,
    LFormSelect
  },
  mixins: [gamesMixin, formMixin],
  data() {
    return {
      game: this.initGame(),
      games: [],
      form: {
        location: '',
        owner_id: '',
        notes: '',
        game_id: '',
      },
      options: {
        isMultipleGamesActive: false,
        isKeepOwnerActive: false,
        isAddMoreGamesActive: false,
      },
      player: {},
    }
  },
  watch: {},
  methods: {
    initGame() {
      return {
        id: '',
        name: '',
        thumbnail: '',
      }
    },
    assignGame(game) {
      bggService.fetch(game.id).then(response => {
        this.game = response
        this.form.game_id = game.id
        this.$bvModal.hide('game-select-modal')
      })
    },
    assignPlayer(player) {
      this.player = player
      this.form.owner_id = player.id
      this.$bvModal.hide('player-select-modal')
    },
    onSubmit() {
      this.$v.form.$touch()
      if (this.$v.form.$anyError) {
        return
      }

      this.form.game_id = this.game.id
      this.form.owner_id = this.player.id

      libraryService
        .createGame(this.form)
        .then(() => {
          this.$toast.success('Saved')
          this.$router.push({ name: 'Home' })
        })
        .catch(response => console.log(response))
    },
  },
  validations: {
    form: {
      game_id: {
        required,
      },
      owner_id: {
        required,
      },
      location: {
        required,
      },
    },
  },
}
</script>

<style scoped></style>
