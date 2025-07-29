<template>
  <div class="modal fade" id="parkingLotDetailsModal" tabindex="-1">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">
            <i class="fas fa-building me-2"></i>
            {{ parkingLot?.prime_location_name || 'Parking Lot Details' }}
          </h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" @click="closeModal"></button>
        </div>
        
        <div class="modal-body">
          <div class="row">
            <!-- Left Column - Basic Information -->
            <div class="col-lg-6">
              <div class="card border-left-primary h-100">
                <div class="card-header">
                  <h6 class="m-0 font-weight-bold text-primary">
                    <i class="fas fa-info-circle me-2"></i>
                    Basic Information
                  </h6>
                </div>
                <div class="card-body">
                  <div class="row mb-3">
                    <div class="col-sm-4">
                      <strong>Location Name:</strong>
                    </div>
                    <div class="col-sm-8">
                      {{ parkingLot?.prime_location_name || 'N/A' }}
                    </div>
                  </div>
                  
                  <div class="row mb-3">
                    <div class="col-sm-4">
                      <strong>Address:</strong>
                    </div>
                    <div class="col-sm-8">
                      {{ parkingLot?.address || 'N/A' }}
                    </div>
                  </div>
                  
                  <div class="row mb-3">
                    <div class="col-sm-4">
                      <strong>Pin Code:</strong>
                    </div>
                    <div class="col-sm-8">
                      <span class="badge bg-secondary">{{ parkingLot?.pin_code || 'N/A' }}</span>
                    </div>
                  </div>
                  
                  <div class="row mb-3">
                    <div class="col-sm-4">
                      <strong>Price per Hour:</strong>
                    </div>
                    <div class="col-sm-8">
                      <span class="badge bg-success">₹{{ parkingLot?.price || 0 }}/hr</span>
                    </div>
                  </div>
                  
                  <div class="row mb-3">
                    <div class="col-sm-4">
                      <strong>Status:</strong>
                    </div>
                    <div class="col-sm-8">
                      <span 
                        class="badge"
                        :class="parkingLot?.is_active ? 'bg-success' : 'bg-secondary'"
                      >
                        {{ parkingLot?.is_active ? 'Active' : 'Inactive' }}
                      </span>
                    </div>
                  </div>
                  
                  <div class="row mb-3" v-if="parkingLot?.description">
                    <div class="col-sm-4">
                      <strong>Description:</strong>
                    </div>
                    <div class="col-sm-8">
                      {{ parkingLot.description }}
                    </div>
                  </div>
                  
                  <div class="row mb-3" v-if="parkingLot?.operating_hours_start || parkingLot?.operating_hours_end">
                    <div class="col-sm-4">
                      <strong>Operating Hours:</strong>
                    </div>
                    <div class="col-sm-8">
                      {{ parkingLot?.operating_hours_start || 'N/A' }} - {{ parkingLot?.operating_hours_end || 'N/A' }}
                    </div>
                  </div>
                  
                  <div class="row">
                    <div class="col-sm-4">
                      <strong>Created:</strong>
                    </div>
                    <div class="col-sm-8">
                      {{ formatDate(parkingLot?.created_at) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Right Column - Parking Spots -->
            <div class="col-lg-6">
              <div class="card border-left-info h-100">
                <div class="card-header d-flex justify-content-between align-items-center">
                  <h6 class="m-0 font-weight-bold text-info">
                    <i class="fas fa-th me-2"></i>
                    Parking Spots
                  </h6>
                  <div>
                    <span class="badge bg-success me-1">{{ availableSpots }} Available</span>
                    <span class="badge bg-danger">{{ occupiedSpots }} Occupied</span>
                  </div>
                </div>
                <div class="card-body">
                  <!-- Spots Statistics -->
                  <div class="row mb-4">
                    <div class="col-md-4 text-center">
                      <div class="h4 text-primary">{{ totalSpots }}</div>
                      <small class="text-muted">Total Spots</small>
                    </div>
                    <div class="col-md-4 text-center">
                      <div class="h4 text-success">{{ availableSpots }}</div>
                      <small class="text-muted">Available</small>
                    </div>
                    <div class="col-md-4 text-center">
                      <div class="h4 text-danger">{{ occupiedSpots }}</div>
                      <small class="text-muted">Occupied</small>
                    </div>
                  </div>
                  
                  <!-- Occupancy Rate -->
                  <div class="mb-4">
                    <label class="form-label small text-muted">Occupancy Rate</label>
                    <div class="progress mb-2">
                      <div 
                        class="progress-bar"
                        :class="occupancyRate > 80 ? 'bg-danger' : occupancyRate > 50 ? 'bg-warning' : 'bg-success'"
                        :style="{ width: occupancyRate + '%' }"
                      ></div>
                    </div>
                    <small class="text-muted">{{ occupancyRate.toFixed(1) }}% occupied</small>
                  </div>
                  
                  <!-- Spots Grid Visualization -->
                  <div class="spots-visualization">
                    <label class="form-label small text-muted mb-3">Spots Layout</label>
                    <div class="spots-grid">
                      <div 
                        v-for="spot in parkingSpots" 
                        :key="spot.id"
                        class="spot-card"
                        :class="{
                          'available': spot.status === 'A',
                          'occupied': spot.status === 'O'
                        }"
                        :title="`Spot ${spot.id}: ${spot.status === 'A' ? 'Available' : 'Occupied'}`"
                      >
                        <i class="fas fa-car"></i>
                        <small>{{ spot.id }}</small>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Legend -->
                  <div class="mt-3">
                    <small class="text-muted">
                      <span class="badge bg-success me-2">Available</span>
                      <span class="badge bg-danger">Occupied</span>
                    </small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="closeModal">
            <i class="fas fa-times me-1"></i>
            Close
          </button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="editParkingLot"
          >
            <i class="fas fa-edit me-1"></i>
            Edit Parking Lot
          </button>
          <button 
            type="button" 
            class="btn btn-danger" 
            @click="deleteParkingLot"
            :disabled="!canDelete"
          >
            <i class="fas fa-trash me-1"></i>
            Delete Parking Lot
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'

const props = defineProps({
  parkingLot: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['modal-closed', 'edit-parking-lot', 'delete-parking-lot'])

// Computed properties for spots statistics
const parkingSpots = computed(() => props.parkingLot?.parking_spots || [])
const totalSpots = computed(() => props.parkingLot?.number_of_spots || 0)
const availableSpots = computed(() => parkingSpots.value.filter(spot => spot.status === 'A').length)
const occupiedSpots = computed(() => parkingSpots.value.filter(spot => spot.status === 'O').length)
const occupancyRate = computed(() => totalSpots.value > 0 ? (occupiedSpots.value / totalSpots.value) * 100 : 0)
const canDelete = computed(() => occupiedSpots.value === 0)

// MOVE FUNCTIONS BEFORE THE WATCH
const showModal = async () => {
  await nextTick()
  const modalElement = document.getElementById('parkingLotDetailsModal')
  console.log('Details Modal element found:', modalElement)
  console.log('Bootstrap available:', window.bootstrap)
  
  if (modalElement) {
    if (window.bootstrap && window.bootstrap.Modal) {
      const modal = new window.bootstrap.Modal(modalElement)
      modal.show()
      
      // Listen for modal hidden event
      modalElement.addEventListener('hidden.bs.modal', closeModal, { once: true })
    } else {
      console.error('Bootstrap not available for details modal!')
    }
  } else {
    console.error('Details modal element not found!')
  }
}

const closeModal = () => {
  const modalElement = document.getElementById('parkingLotDetailsModal')
  if (modalElement) {
    if (window.bootstrap && window.bootstrap.Modal) {
      const modal = window.bootstrap.Modal.getInstance(modalElement)
      if (modal) {
        modal.hide()
      }
    }
  }
  emit('modal-closed')
}

const editParkingLot = () => {
  closeModal()
  emit('edit-parking-lot', props.parkingLot)
}

const deleteParkingLot = () => {
  if (!canDelete.value) {
    alert('Cannot delete parking lot with occupied spots!')
    return
  }
  
  if (confirm(`Are you sure you want to delete "${props.parkingLot.prime_location_name}"?`)) {
    closeModal()
    emit('delete-parking-lot', props.parkingLot)
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

// NOW THE WATCH CAN SAFELY CALL showModal
watch(() => props.parkingLot, (newParkingLot) => {
  if (newParkingLot) {
    showModal()
  }
}, { immediate: true })
</script>

<style scoped>
.border-left-primary {
  border-left: 0.25rem solid var(--bs-primary) !important;
}

.border-left-info {
  border-left: 0.25rem solid var(--bs-info) !important;
}

.spots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
  gap: 8px;
  max-height: 300px;
  overflow-y: auto;
}

.spot-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8px;
  border: 2px solid;
  border-radius: 8px;
  height: 60px;
  transition: all 0.2s;
  cursor: pointer;
}

.spot-card.available {
  background-color: rgba(var(--bs-success-rgb), 0.1);
  border-color: var(--bs-success);
  color: var(--bs-success);
}

.spot-card.occupied {
  background-color: rgba(var(--bs-danger-rgb), 0.1);
  border-color: var(--bs-danger);
  color: var(--bs-danger);
}

.spot-card:hover {
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.spot-card i {
  font-size: 1.2rem;
  margin-bottom: 2px;
}

.spot-card small {
  font-weight: bold;
  font-size: 0.7rem;
}
</style>