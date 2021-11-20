<template>
  <b-form-input
      :value="formattedValue"
      ref="inputRef"
      placeholder="Insert an amount"
      @input="$emit('input', $event)"
      :class="{'is-invalid': state === false}"
  />

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
      exportValueAsInteger: true,
      precision: 2,
      currencyDisplay: 'hidden'
    })

    return { inputRef, formattedValue }
  },
  components: {

  }
}
</script>

<style scoped>

</style>