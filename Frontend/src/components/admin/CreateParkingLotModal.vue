<template>
  <div class="modal fade" id="createParkingLotModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="fas fa-building me-2"></i>
            Create New Parking Lot
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        
        <form @submit.prevent="createParkingLot">
          <div class="modal-body">
            <!-- Form content matching your wireframe -->
            <div class="accordion" id="createParkingLotAccordion">
              <!-- Basic Information -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button 
                    class="accordion-button" 
                    type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#basicInfo" 
                    aria-expanded="true"
                  >
                    <i class="fas fa-info-circle me-2"></i>
                    Basic Information
                  </button>
                </h2>
                <div id="basicInfo" class="accordion-collapse collapse show" data-bs-parent="#createParkingLotAccordion">
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
                    data-bs-target="#parkingDetails"
                  >
                    <i class="fas fa-car me-2"></i>
                    Parking Details
                  </button>
                </h2>
                <div id="parkingDetails" class="accordion-collapse collapse" data-bs-parent="#createParkingLotAccordion">
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
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Cancel
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="fas fa-save me-2"></i>
              {{ loading ? 'Creating...' : 'Create Parking Lot' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'

const emit = defineEmits(['parking-lot-created'])

const loading = ref(false)
const formData = reactive({
  prime_location_name: '',
  address: '',
  pin_code: '',
  number_of_spots: 10,
  price: 50
})

const createParkingLot = async () => {
  loading.value = true
  
  try {
    await axios.post('/api/admin/pkl/create', formData)
    
    // Reset form
    Object.assign(formData, {
      prime_location_name: '',
      address: '',
      pin_code: '',
      number_of_spots: 10,
      price: 50
    })
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('createParkingLotModal'))
    modal.hide()
    
    emit('parking-lot-created')
    
  } catch (error) {
    alert(error.response?.data?.message || 'Error creating parking lot')
  } finally {
    loading.value = false
  }
}
</script>