<template>
  <!-- Filters trigger -->
  <b-col cols="auto">
    <b-button
      v-b-toggle:[collapseId]
      :pressed.sync="filtersOpen"
      aria-expanded="false"
      aria-haspopup="true"
      class="btn-white"
      data-toggle="dropdown"
      size="lg"
    >
      <b-icon-filter/>
      Filters
      <b-badge v-show="showFiltersBadge" class="ml-1">{{
        filters.count()
      }}</b-badge>
    </b-button>
  </b-col>
</template>

<script>
import usersMixin from '@/mixins/users.mixin'

export default {
  name: 'FiltersButton',
  mixins: [usersMixin],
  props: {
    collapseId: {
      type: String,
      default: 'filters-collapse',
    },
    filters: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      filtersOpen: false,
    }
  },
  computed:{
    showFiltersBadge(){
      return this.filters.count() > 0
    }
  }
}
</script>
