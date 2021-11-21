<template>
  <filter-item :label="label">
    <b-form-radio-group class="w-100"
        button-variant="white"
        v-model="filtersModel.filtersSelected[id]"
        :options="options"
        buttons
    />
  </filter-item>
</template>

<script>
import FilterItem from "@/components/filters/FilterItem"
import Filters from "@/components/filters/Filters"

export default {
  name: "FilterRadioButton",
  components: {
    FilterItem
  },
  props: {
    value: {
      type: Filters.Model,
      required: true,
    },
    id: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      default: '',
    },
    options: {
      type: Array,
      default: () => [],
    },
  },
  computed: {
    filtersModel: {
      get() {
        return this.value
      },
      set(value) {
        this.$emit('input', value)
      },
    },
  },
}
</script>

<style scoped>

</style>