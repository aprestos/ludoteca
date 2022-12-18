<template>
  <div class="main-content">
    <div class="pt-4 pb-5 bg-hero">
      <div class="container-fluid">

          <div class="d-flex justify-content-between">
            <div class="d-flex align-content-center align-items-center " style="flex-basis: 0; flex-grow: 1">
            </div>
            <b-link :to="{'name': 'Home'}">
            <img src="@/assets/whitelogo.png" style="width: 6rem"/>
            </b-link>
            <div style="flex-basis: 0; flex-grow: 1" class="d-flex justify-content-end">
            </div>

        </div> <!-- / .row -->
      </div>
    </div>

    <div class="container-fluid">

      <!-- User -->
      <div class="container-lg container-fluid">
        <div class="row justify-content-center">
          <div class="col-12 col-lg-10 col-xl-8">

            <!-- Form -->
            <form class="tab-content py-6" id="wizardSteps">
              <div class="tab-pane fade show active" id="wizardStepOne" role="tabpanel"
                   aria-labelledby="wizardTabOne">

                <!-- Header -->
                <div class="row justify-content-center">
                  <div class="col-12 col-md-10 col-lg-8 col-xl-6 text-center">

                    <!-- Pretitle -->
                    <h6 class="mb-4 text-uppercase text-muted">
                      Step {{ currentStep }} of {{ numberOfSteps }}
                    </h6>

                    <!-- Title -->
                    <h1 class="mb-3">
                      {{ title }}
                    </h1>

                    <!-- Subtitle -->
                    <p class="mb-5 text-muted">
                      {{ description }}
                    </p>

                  </div>
                </div> <!-- / .row -->

                <slot name="content"></slot>

                <!-- Divider -->
                <hr class="my-5">

                <!-- Footer -->
                <div class="d-flex justify-content-between align-items-center">
                  <div style="flex-grow: 1; flex-basis: 0">

                    <!-- Button -->
                    <b-button v-if="currentStep>1" size="lg" variant="white" @click="$emit('previous')">Previous</b-button>

                  </div>
                  <div class="text-center">

                    <!-- Step -->
                    <h6 class="text-uppercase text-muted mb-0">Step {{currentStep}} of {{numberOfSteps}}</h6>

                  </div>
                  <div style="flex-grow: 1; flex-basis: 0" class="d-flex justify-content-end">

                    <!-- Button -->
                    <b-button
                        v-if="currentStep<numberOfSteps"
                        size="lg"
                        variant="primary"
                        data-toggle="wizard"
                        @click="$emit('next')"
                    >Continue</b-button>
                    <b-button
                        v-else
                        size="lg"
                        variant="primary"
                        data-toggle="wizard"
                        @click="$emit('finish')"
                        :disabled="loading"
                    ><b-spinner v-show="loading" small/><span v-show="!loading">Finish</span></b-button>

                  </div>
                </div>

              </div>
            </form>

          </div>
        </div>
      </div>

    </div>
  </div>

</template>

<script>

export default {
  name: "Wizard",
  props: {
    title: String,
    description: String,
    currentStep: Number,
    numberOfSteps: Number,
    loading: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>

</style>
