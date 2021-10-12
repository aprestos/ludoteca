<template>
  <div class="min-vh-100">
    <div class="bg-white shadow-sm">
    <b-container>
      <b-row class="py-3 align-items-center">
        <b-col cols="auto">
          <b-button size="lg" :to="backTo" variant="light" class="btn-rounded-circle">
            <span class="fe fe-arrow-left"></span></b-button>
        </b-col>
        <b-col>
          <div class="d-flex flex-column">
<!--            <b-breadcrumb :items="breadcrumb"/>-->
            <h6 class="header-pretitle">{{preTitle}}</h6>
            <h1 class="header-title mb-2">
            {{ title }}
          </h1>
          </div>
        </b-col>
      </b-row>

    </b-container>
      </div>
    <b-container class="pt-5">
      <b-row class="justify-content-center">
        <b-col lg="10" md="12" xl="8">
          <slot> </slot>
        </b-col>
      </b-row>
    </b-container>
    <b-container class="">
      <b-row class="justify-content-center">
        <b-col lg="10" md="10" sm="12" xl="8">
          <form novalidate @submit.stop.prevent="onSubmit">
          <slot name="content"></slot>
                </form>
        </b-col>
      </b-row>
    </b-container>
    <b-container class="fixed-bottom position-fixed py-5">
      <b-row class="justify-content-center">
        <b-col lg="10" md="10" sm="12" xl="8">
            <div class="d-flex flex-row">
              <b-button
                variant="secondary"
                size="lg"
                :to="{ name: 'LibraryHome' }"
                >Cancel</b-button
              >
              <b-button
                variant="primary"
                size="lg"
                class="ml-5"
                block
                v-on:click="onSubmit()"
              >
                Finish
              </b-button>
              </div>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'InputScreen',
  components: {},
  props: {
    preTitle: {
      type: String,
      default: ''
    },
    title: {},
    subTitle: {},
    breadcrumb: [],
    backTo: {
      type: Object,
    },
  },
  methods:{
    onSubmit(){
      this.$emit('submit')
    }
  }
}
</script>

<style scoped>
</style>
