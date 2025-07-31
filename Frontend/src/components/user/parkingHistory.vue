// frontend/src/components/User/ParkingHistory.vue
<template>
  <div class="card">
    <div class="card-header">
      <h5>Export Parking History</h5>
    </div>
    <div class="card-body">
      <button 
        @click="exportCSV" 
        :disabled="exporting"
        class="btn btn-primary"
      >
        <i class="fas fa-download"></i>
        {{ exporting ? 'Exporting...' : 'Export as CSV' }}
      </button>
      
      <div v-if="exportStatus" class="mt-3">
        <div class="progress">
          <div 
            class="progress-bar" 
            :style="`width: ${exportProgress}%`"
          >
            {{ exportProgress }}%
          </div>
        </div>
        <small class="text-muted">{{ exportStatus }}</small>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const authStore = useAuthStore()

// Reactive data
const exporting = ref(false)
const exportTaskId = ref(null)
const exportProgress = ref(0)
const exportStatus = ref('')

// Methods
const exportCSV = async () => {
  try {
    exporting.value = true
    
    const response = await axios.post('/api/user/export-csv', {
      user_id: authStore.user?.id,
      email: authStore.user?.email
    })
    
    if (response.data.success) {
      exportTaskId.value = response.data.task_id
      checkExportStatus()
    }
  } catch (error) {
    console.error('Export failed:', error)
    exporting.value = false
  }
}

const checkExportStatus = async () => {
  try {
    const response = await axios.post(`/api/user/export-status`)
    const data = response.data
    
    if (data.state === 'PROGRESS') {
      exportProgress.value = data.current
      exportStatus.value = data.status
      setTimeout(() => checkExportStatus(), 1000)
    } else if (data.state === 'SUCCESS') {
      exportProgress.value = 100
      exportStatus.value = 'Export completed! Check your email for download link.'
      exporting.value = false
    } else if (data.state === 'FAILURE') {
      exportStatus.value = `Export failed: ${data.error}`
      exporting.value = false
    }
  } catch (error) {
    console.error('Status check failed:', error)
    exporting.value = false
  }
}
</script>