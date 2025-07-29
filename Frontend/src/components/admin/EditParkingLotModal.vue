<template>
  <div class="modal fade" id="editParkingLotModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="fas fa-edit me-2"></i>
            Edit Parking Lot
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" @click="closeModal"></button>
        </div>
        
        <form @submit.prevent="updateParkingLot">
          <div class="modal-body">
            <!-- Alert for Success/Error -->
            <div v-if="successMessage" class="alert alert-success alert-dismissible fade show" role="alert">
              <i class="fas fa-check-circle me-2"></i>
              {{ successMessage }}
              <button type="button" class="btn-close" @click="successMessage = ''"></button>
            </div>
            
            <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show" role="alert">
              <i class="fas fa-exclamation-triangle me-2"></i>
              {{ errorMessage }}
              <button type="button" class="btn-close" @click="errorMessage = ''"></button>
            </div>

            <!-- Form content using accordion like create modal -->
            <div class="accordion" id="editParkingLotAccordion">
              <!-- Basic Information -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button 
                    class="accordion-button" 
                    type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#editBasicInfo" 
                    aria-expanded="true"
                  >
                    <i class="fas fa-info-circle me-2"></i>
                    Basic Information
                  </button>
                </h2>
                <div id="editBasicInfo" class="accordion-collapse collapse show" data-bs-parent="#editParkingLotAccordion">
                  <div class="accordion-body">
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label class="form-label">Prime Location Name *</label>
                        <input 
                          type="text" 
                          class="form-control"
                          v-model="formData.prime_location_name"
                          required
                        >
                      </div>
                      <div class="col-md-6 mb-3">
                        <label class="form-label">Pin Code *</label>
                        <input 
                          type="text" 
                          class="form-control"
                          v-model="formData.pin_code"
                          pattern="[0-9]{6}"
                          required
                        >
                      </div>
                    </div>
                    
                    <div class="mb-3">
                      <label class="form-label">Address *</label>
                      <textarea 
                        class="form-control" 
                        rows="3"
                        v-model="formData.address"
                        required
                      ></textarea>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Parking Details -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button 
                    class="accordion-button collapsed" 
                    type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#editParkingDetails"
                  >
                    <i class="fas fa-car me-2"></i>
                    Parking Details
                  </button>
                </h2>
                <div id="editParkingDetails" class="accordion-collapse collapse" data-bs-parent="#editParkingLotAccordion">
                  <div class="accordion-body">
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label class="form-label">Number of Spots *</label>
                        <input 
                          type="number" 
                          class="form-control"
                          v-model.number="formData.number_of_spots"
                          min="1"
                          max="100"
                          required
                        >
                        <div class="form-text">
                          <i class="fas fa-info-circle me-1"></i>
                          Current spots: {{ parkingLot?.number_of_spots || 0 }}
                        </div>
                      </div>
                      <div class="col-md-6 mb-3">
                        <label class="form-label">Price per Hour (₹) *</label>
                        <input 
                          type="number" 
                          class="form-control"
                          v-model.number="formData.price"
                          min="1"
                          step="0.01"
                          required
                        >
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Additional Settings -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button 
                    class="accordion-button collapsed" 
                    type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#editAdditionalSettings"
                  >
                    <i class="fas fa-cog me-2"></i>
                    Additional Settings
                  </button>
                </h2>
                <div id="editAdditionalSettings" class="accordion-collapse collapse" data-bs-parent="#editParkingLotAccordion">
                  <div class="accordion-body">
                    <div class="row">
                      <div class="col-md-12 mb-3">
                        <label class="form-label">Description</label>
                        <textarea 
                          class="form-control" 
                          rows="2"
                          v-model="formData.description"
                          placeholder="Optional description for the parking lot"
                        ></textarea>
                      </div>
                    </div>
                    
                    <div class="row">
                      <div class="col-md-6 mb-3">
                        <label class="form-label">Operating Hours Start</label>
                        <input 
                          type="time" 
                          class="form-control"
                          v-model="formData.operating_hours_start"
                        >
                      </div>
                      <div class="col-md-6 mb-3">
                        <label class="form-label">Operating Hours End</label>
                        <input 
                          type="time" 
                          class="form-control"
                          v-model="formData.operating_hours_end"
                        >
                      </div>
                    </div>
                    
                    <div class="mb-3 form-check">
                      <input 
                        type="checkbox" 
                        class="form-check-input" 
                        id="isActiveCheck"
                        v-model="formData.is_active"
                      >
                      <label class="form-check-label" for="isActiveCheck">
                        <i class="fas fa-toggle-on me-1"></i>
                        Active (Available for bookings)
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeModal">
              <i class="fas fa-times me-1"></i>
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="fas fa-save me-2"></i>
              {{ loading ? 'Updating...' : 'Update Parking Lot' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted, nextTick } from 'vue'
import axios from 'axios'

const props = defineProps({
  parkingLot: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['parking-lot-updated', 'modal-closed'])

const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const formData = reactive({
  prime_location_name: '',
  address: '',
  pin_code: '',
  number_of_spots: 10,
  price: 50,
  // description: '',
  // operating_hours_start: '',
  // operating_hours_end: '',
  is_active: true
})

const populateForm = (lot) => {
  Object.assign(formData, {
    prime_location_name: lot.prime_location_name || '',
    address: lot.address || '',
    pin_code: lot.pin_code || '',
    number_of_spots: lot.number_of_spots || 10,
    price: lot.price || 50,
    // description: lot.description || '',
    // operating_hours_start: lot.operating_hours_start || '',
    // operating_hours_end: lot.operating_hours_end || '',
    is_active: lot.is_active !== undefined ? lot.is_active : true
  })
}

const showModal = async () => {
  await nextTick()
  const modalElement = document.getElementById('editParkingLotModal')
  
  if (modalElement) {
    if (window.bootstrap && window.bootstrap.Modal) {
      const modal = new window.bootstrap.Modal(modalElement)
      modal.show()

      // Listen for modal hidden event
      modalElement.addEventListener('hidden.bs.modal', closeModal, { once: true })
    } else {
      console.error('Bootstrap not available!')
    }
  } else {
    console.error('Modal element not found!')
  }
}

const updateParkingLot = async () => {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  
  try {
    const response = await axios.post(`/api/admin/pkl/update/${props.parkingLot.id}`, formData)
    
    successMessage.value = 'Parking lot updated successfully!'
    
    // Close modal after short delay
    setTimeout(() => {
      closeModal()
      emit('parking-lot-updated')
    }, 1500)
    
  } catch (error) {
    errorMessage.value = error.response?.data?.message || 'Error updating parking lot'
  } finally {
    loading.value = false
  }
}

const closeModal = () => {
  const modalElement = document.getElementById('editParkingLotModal')
  if (modalElement) {
    const modal = window.bootstrap.Modal.getInstance(modalElement)
    if (modal) {
      modal.hide()
    }
  }
  emit('modal-closed')
}

// Watch for prop changes and populate form + show modal
watch(() => props.parkingLot, async (newParkingLot) => {
  if (newParkingLot) {
    populateForm(newParkingLot)
    await nextTick()
    showModal()
  }
}, { immediate: true })

onMounted(async () => {
  if (props.parkingLot) {
    populateForm(props.parkingLot)
    await nextTick()
    showModal()
  }
})
</script>

<style scoped>
.accordion-button:not(.collapsed) {
  background-color: rgba(var(--bs-primary-rgb), 0.1);
  border-color: var(--bs-primary);
}

.form-check-input:checked {
  background-color: var(--bs-success);
  border-color: var(--bs-success);
}
</style>
