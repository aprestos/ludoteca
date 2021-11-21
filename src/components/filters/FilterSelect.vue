<template>
  <filter-item :label="label">
      <FormSelect
          v-model="filtersModel.filtersSelected[id]"
          :options="options"
          option-text="name"
          option-value="id"
      />
  </filter-item>
</template>

<script>
import FormSelect from '@/components/FormSelect'
import Filters from '@/components/filters/Filters'
import FilterItem from "@/components/filters/FilterItem"

export default {
  name: 'FilterSelect',
  components: {FormSelect, FilterItem},
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
