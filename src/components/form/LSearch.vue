<template>
    <div class="input-group input-group-lg input-group-merge">
      <b-form-input
          v-model="term"
          class="form-control-appended form-control-prepended"
          debounce="500"
          placeholder="Search"
          type="search"
      />
      <div class="input-group-prepend">
        <div class="input-group-text">
          <b-icon-search font-scale="0.8"/>
        </div>
      </div>
      <div class="input-group-append">
        <div class="input-group-text">
          <b-link>
          <b-icon-x v-if="value" @click="$emit('input', '')"/>
            </b-link>
        </div>
      </div>
    </div>
</template>

<script>
export default {
  name: "LSearch",
  props: {
    value: {
      type: String
    }
  },
  computed: {
    term: {
      get(){
        return this.value
      },
      set(value){
        this.$emit('input', value)
      }
    }
  }
}
</script>

<style scoped>

</style>
