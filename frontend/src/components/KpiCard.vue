<script setup>
import {
  TrendingUp,
  TrendingDown
} from "lucide-vue-next"

defineProps({
  title: {
    type: String,
    required: true
  },

  value: {
    type: [String, Number],
    required: true
  },

  subtitle: {
    type: String,
    default: ""
  },

  trend: {
    type: Number,
    default: null
  },

  icon: {
    type: Object,
    default: null
  }
})
</script>

<template>
  <div class="kpi-card">

    <div class="kpi-top">

      <div class="kpi-icon">
        <component
          v-if="icon"
          :is="icon"
          :size="20"
          :stroke-width="1.8"
        />
      </div>

      <div
        v-if="trend !== null"
        class="kpi-trend"
        :class="trend >= 0 ? 'positive' : 'negative'"
      >
        <TrendingUp
          v-if="trend >= 0"
          :size="14"
        />

        <TrendingDown
          v-else
          :size="14"
        />

        {{ Math.abs(trend) }}%
      </div>

    </div>

    <div class="kpi-title">
      {{ title }}
    </div>

    <div class="kpi-value">
      {{ value }}
    </div>

    <div
      v-if="subtitle"
      class="kpi-subtitle"
    >
      {{ subtitle }}
    </div>

  </div>
</template>