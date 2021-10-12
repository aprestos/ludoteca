<template>
  <b-form-input
      :value="formattedValue"
      size="lg"
      ref="inputRef"
      placeholder="Insert an amount"
      @input="$emit('input', $event)"
      :class="{'is-invalid': state === false}"
  />

<!--  <currency-input-->
<!--      class="form-control form-control-lg"-->
<!--      placeholder="Insert an amount"-->
<!--      :value="value"-->
<!--      :state="state"-->
<!--      :class="{'is-invalid': state === false}"-->
<!--      @input="$emit('input', $event)"/>-->
</template>

<script>
import { useCurrencyInput } from 'vue-currency-input'

export default {
  name: "LFormCurrency",
  props: {
    options: Object,
    value: {
      required: true
    },
    state: {
      default: true
    }
  },
  setup () {
    const { formattedValue, inputRef } = useCurrencyInput({
    currency: 'EUR',
    hideCurrencySymbolOnFocus: true,
    hideGroupingSeparatorOnFocus: true,
    hideNegligibleDecimalDigitsOnFocus: true,
    precision: 2
    })

    return { inputRef, formattedValue }
  },
  components: {

  }
}
</script>

<style scoped>

</style>