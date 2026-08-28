<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },

  subtitle: {
    type: String,
    default: ""
  },

  span: {
    type: String,
    default: ""
  }
})
</script>

<template>
  <section
    class="report-card"
    :class="span"
  >

    <div class="report-card-header">

      <div>
        <h3>
          {{ title }}
        </h3>

        <p v-if="subtitle">
          {{ subtitle }}
        </p>
      </div>

      <slot name="header" />

    </div>

    <div class="report-card-content">
      <slot />
    </div>

  </section>
</template>