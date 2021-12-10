<template>
<div class="position-relative">
  <div class="position-absolute top left right h-100 w-100 bg-success-soft d-flex align-items-center justify-content-center"
       v-if="location.type === 'room'"
       style="opacity: 50%">
    <h1 class="">{{ location.name }}</h1>
  </div>
  <div class="d-flex-row">
    <div class="d-flex flex-row" v-for="(row, index) in rows" v-bind:key="index">
      <div
        v-for="(column, index) in columns"
        v-bind:key="index"
        :class="{
          'bg-light': !isLocationCell(column, row),
          'bg-success': isLocationCell(column, row),
        }"
        class="m-1 flex-grow-1 shelf"
        style="flex-basis: 0"
      >
        <span
          v-if="isLocationCell(column, row)"
          class="text-white"
          ><b-icon-geo-fill class="d-sm-inline d-none"/> {{ location.name }}</span
        >
      </div>
    </div>
  </div>
  </div>
</template>

<script>
export default {
  name: 'LocationShelves',
  props: {
    location: {
      type: Object
    },
  },
  computed: {
    columns() {
      const columns = []
      const shelves = this.$store.getters['library/locations'].filter(
        (item) => item.type === 'shelf',
      )
      shelves.forEach((shelf) => {
        const column = shelf.name.substring(0, 1)

        if (!columns.includes(column)) {
          columns.push(column)
        }

        columns.sort()
      })
      return columns
    },
    rows() {
      const rows = []
      const shelves = this.$store.getters['library/locations'].filter(
        (item) => item.type === 'shelf',
      )
      shelves.forEach((shelf) => {
        const row = shelf.name.substring(1, 2)

        if (!rows.includes(row)) {
          rows.push(row)
        }

        rows.sort()
      })
      return rows
    },
  },
  methods: {
    isLocationCell(column, row) {
      return column + row === this.location.name
    },
  },
}
</script>

<style scoped>
.shelf {
  border-radius: 5px;
  height: 5vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
