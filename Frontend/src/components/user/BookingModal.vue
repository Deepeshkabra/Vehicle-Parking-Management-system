<template>
  <div class="modal fade show d-block" tabindex="-1" style="background-color: rgba(0,0,0,0.5)">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header bg-primary text-white">
          <h5 class="modal-title">Book Parking Spot</h5>
          <button type="button" class="btn-close btn-close-white" @click="$emit('modal-closed')"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="confirmBooking">
            <div class="mb-3">
              <label class="form-label">Spot ID:</label>
              <input type="text" class="form-control" :value="nextAvailableSpot" readonly>
            </div>
            <div class="mb-3">
              <label class="form-label">Lot ID:</label>
              <input type="text" class="form-control" :value="parkingLot.id" readonly>
            </div>
            <div class="mb-3">
              <label class="form-label">User ID:</label>
              <input type="text" class="form-control" :value="authStore.user?.id" readonly>
            </div>
            <div class="mb-3">
              <label class="form-label">Vehicle Number: *</label>
              <input 
                type="text" 
                class="form-control" 
                v-model="vehicleNumber"
                placeholder="Enter vehicle number"
                required
              >
            </div>
            <div class="mb-3">
              <label class="form-label">Location:</label>
              <input type="text" class="form-control" :value="parkingLot.prime_location_name" readonly>
            </div>
            <div class="mb-3">
              <label class="form-label">Price:</label>
              <input type="text" class="form-control" :value="`₹${parkingLot.price}/hr`" readonly>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="$emit('modal-closed')">Cancel</button>
          <button type="button" class="btn btn-primary" @click="confirmBooking" :disabled="!vehicleNumber">
            Reserve
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'

const props = defineProps(['parkingLot'])
const emit = defineEmits(['booking-confirmed', 'modal-closed'])

const authStore = useAuthStore()
const vehicleNumber = ref('')

const nextAvailableSpot = computed(() => {
  return 'Auto-assigned'
})

const confirmBooking = async () => {
  try {
    const response = await axios.post(`/api/user/pkl/book/${props.parkingLot.id}`, {
      vehicle_number: vehicleNumber.value
    })
    
    if (response.data.success) {
      alert('Booking confirmed successfully!')
      emit('booking-confirmed')
    }
  } catch (error) {
    alert(error.response?.data?.message || 'Booking failed')
  }
}
</script>