<template>
  <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header bg-warning text-dark">
          <h5 class="modal-title">Release Parking Spot</h5>
          <button type="button" class="btn-close" @click="$emit('modal-closed')"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">Spot ID:</label>
            <input type="text" class="form-control" :value="booking.spot_id" readonly>
          </div>
          <div class="mb-3">
            <label class="form-label">Vehicle Number:</label>
            <input type="text" class="form-control" :value="booking.vehicle_number" readonly>
          </div>
          <div class="mb-3">
            <label class="form-label">Parking Time:</label>
            <input type="text" class="form-control" :value="formatDateTime(booking.parking_timestamp)" readonly>
          </div>
          <div class="mb-3">
            <label class="form-label">Releasing Time:</label>
            <input type="text" class="form-control" :value="new Date().toLocaleString()" readonly>
          </div>
          <div class="mb-3">
            <label class="form-label">Total Cost:</label>
            <input type="text" class="form-control" :value="calculateCost()" readonly>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('modal-closed')">Cancel</button>
          <button type="button" class="btn btn-warning" @click="confirmRelease">Release</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'

const props = defineProps(['booking'])
const emit = defineEmits(['release-confirmed', 'modal-closed'])

const calculateCost = () => {
  const startTime = new Date(props.booking.parking_timestamp)
  const endTime = new Date()
  const hours = Math.ceil((endTime - startTime) / (1000 * 60 * 60))
  const cost = hours * (props.booking.hourly_rate || 0)
  return `₹${cost}`
}

const confirmRelease = async () => {
  try {
    const response = await axios.post('/api/user/pkl/release')
    
    if (response.data.success) {
      alert('Parking spot released successfully!')
      emit('release-confirmed')
    }
  } catch (error) {
    alert(error.response?.data?.message || 'Release failed')
  }
}

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString()
}
</script>
