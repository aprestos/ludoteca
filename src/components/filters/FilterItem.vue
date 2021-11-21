<template>
  <b-col lg="6" sm="12">
    <b-form-group :label="label">
      <slot></slot>
    </b-form-group>
  </b-col>
</template>

<script>
export default {
  name: "FilterItem",
  props: {
    label: {
      type: String,
      required: true
    }
  },
}
</script>

<style scoped>

</style>