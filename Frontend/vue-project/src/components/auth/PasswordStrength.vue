<template>
  <div v-if="password" class="password-strength">
    <div class="d-flex justify-content-between align-items-center mb-1">
      <small class="text-muted">Password Strength:</small>
      <small :class="strengthColorClass">{{ strength?.toUpperCase() }}</small>
    </div>
    <div class="progress" style="height: 4px;">
      <div 
        class="progress-bar" 
        :class="strengthProgressClass"
        :style="{ width: strengthPercentage + '%' }"
      ></div>
    </div>
    <div v-if="showErrors && errors.length > 0" class="mt-1">
      <small class="text-muted">Requirements:</small>
      <ul class="small text-muted mb-0 ps-3">
        <li v-for="error in errors" :key="error">
          {{ error }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { validatePassword } from '@/utils/validation';

// Props
interface Props {
  password: string;
  showErrors?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  showErrors: true
});

// Computed properties
const passwordValidation = computed(() => {
  if (!props.password) {
    return { isValid: false, errors: [], strength: 'weak' as const, score: 0 };
  }
  return validatePassword(props.password);
});

const strength = computed(() => passwordValidation.value.strength);
const errors = computed(() => passwordValidation.value.errors);
const isValid = computed(() => passwordValidation.value.isValid);

const strengthPercentage = computed(() => {
  switch (strength.value) {
    case 'weak': return 25;
    case 'medium': return 60;
    case 'strong': return 100;
    default: return 0;
  }
});

const strengthColorClass = computed(() => {
  switch (strength.value) {
    case 'weak': return 'text-danger';
    case 'medium': return 'text-warning';
    case 'strong': return 'text-success';
    default: return 'text-muted';
  }
});

const strengthProgressClass = computed(() => {
  switch (strength.value) {
    case 'weak': return 'bg-danger';
    case 'medium': return 'bg-warning';
    case 'strong': return 'bg-success';
    default: return 'bg-secondary';
  }
});

// Expose validation state for parent components
defineExpose({
  isValid,
  strength,
  errors
});
</script>

<style scoped>
.password-strength {
  margin-top: 0.5rem;
}

.progress {
  border-radius: 2px;
}

.progress-bar {
  transition: width 0.3s ease;
}
</style> 