<template>
        <b-card>
          <div class="d-flex flex-row align-items-center justify-content-between">
            <div class="mr-5">
              <span class="text-uppercase small text-muted mb-2">{{title}}</span>
              <b-skeleton-wrapper :loading="loading">
                <template #loading>
                  <b-skeleton width="2rem"/>
                </template>
                <h2 class="mb-0">{{ value }}</h2>
              </b-skeleton-wrapper>
            </div>
            <b-icon :icon="icon" class="text-muted" font-scale="1.8"/>
          </div>
          <hr/>
          <div class="d-flex flex-row">
            <div class="d-flex flex-row">
              <slot name="metadata"></slot>
            </div>
          </div>

        </b-card>
</template>

<script>
export default {
  name: "NumbersCard",
  props: {
    loading: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      required: true
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