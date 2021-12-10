<template>
          <div class="d-flex flex-row">

              <b-skeleton-wrapper :loading="loading">
                <template #loading>
                  <div class="d-flex flex-row">
                    <b-skeleton class="mr-3" type="avatar" height="1.2rem" width="1.2rem"/>
                    <b-skeleton width="2rem"/>
                  </div>
                </template>
                  <b-icon font-scale="1.3" :icon="icon" class="text-muted mr-3"/>
                <h3 class="mb-0">{{ value }}</h3>
              </b-skeleton-wrapper>
            </div>
</template>

<script>
export default {
  name: "NumbersMetadata",
  props:{
    loading: {
      type: Boolean,
      default: false
    },
    value: {
      required: true
    },
    icon: {
      required: true
    }
  }
}
</script>

<style scoped>

</style>