<template>
  <div class="container-fluid py-4">
    <!-- Header -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h1 class="h3 mb-0 text-gray-800">Admin Dashboard</h1>
            <p class="text-muted">Welcome to Admin {{ authStore.user?.username || 'Admin' }}</p>
          </div>
          <div>
            <button 
              class="btn btn-primary" 
              data-bs-toggle="modal" 
              data-bs-target="#createParkingLotModal"
            >
              <i class="fas fa-plus me-2"></i>
              Add Parking Lot
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                  Total Parking Lots
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  {{ stats.totalLots }}
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-building fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-success shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                  Available Spots
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  {{ stats.availableSpots }}
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-check-circle fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-warning shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                  Occupied Spots
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  {{ stats.occupiedSpots }}
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-car fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-info shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">
                  Registered Users
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  {{ stats.totalUsers }}
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-users fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="row">
      <!-- Parking Lots Grid -->
      <div class="col-lg-8">
        <div class="card shadow mb-4">
          <div class="card-header py-3 d-flex justify-content-between align-items-center">
            <h6 class="m-0 font-weight-bold text-primary">Parking Lots</h6>
            <div class="dropdown">
              <button class="btn btn-link text-muted" data-bs-toggle="dropdown">
                <i class="fas fa-ellipsis-v"></i>
              </button>
              <ul class="dropdown-menu">
                <li><a class="dropdown-item" href="#" @click="refreshParkingLots">Refresh</a></li>
                <li><a class="dropdown-item" href="#" @click="exportData">Export Data</a></li>
              </ul>
            </div>
          </div>
          <div class="card-body">
            <!-- Search and Filter -->
            <div class="row mb-3">
              <div class="col-md-6">
                <div class="input-group">
                  <input 
                    type="text" 
                    class="form-control" 
                    placeholder="Search parking lots..."
                    v-model="searchQuery"
                  >
                  <button class="btn btn-outline-secondary" type="button">
                    <i class="fas fa-search"></i>
                  </button>
                </div>
              </div>
              <div class="col-md-6">
                <select class="form-select" v-model="filterStatus">
                  <option value="">All Status</option>
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                </select>
              </div>
            </div>

            <!-- Parking Lots Grid -->
            <div class="row">
              <div 
                v-for="lot in filteredParkingLots" 
                :key="lot.id" 
                class="col-md-6 col-lg-4 mb-3"
              >
                <div class="card h-100 parking-lot-card">
                  <div class="card-header d-flex justify-content-between align-items-center">
                    <h6 class="mb-0 text-truncate">{{ lot.prime_location_name }}</h6>
                    <span 
                      class="badge"
                      :class="lot.is_active ? 'bg-success' : 'bg-secondary'"
                    >
                      {{ lot.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                  <div class="card-body">
                    <p class="card-text text-muted small mb-2">{{ lot.address }}</p>
                    <div class="mb-2">
                      <small class="text-muted">Pin Code:</small>
                      <span class="fw-bold">{{ lot.pin_code }}</span>
                    </div>
                    <div class="mb-2">
                      <small class="text-muted">Price:</small>
                      <span class="fw-bold text-success">₹{{ lot.price }}/hr</span>
                    </div>
                    
                    <!-- Spots Visualization -->
                    <div class="parking-spots-grid mb-3">
                      <small class="text-muted d-block mb-2">Spots ({{ lot.available_spots }}/{{ lot.number_of_spots }})</small>
                      <div class="spots-container">
                        <div 
                          v-for="spot in lot.parking_spots || []" 
                          :key="spot.id"
                          class="spot-indicator"
                          :class="spot.status === 'A' ? 'available' : 'occupied'"
                          :title="`Spot ${spot.id}: ${spot.status === 'A' ? 'Available' : 'Occupied'}`"
                        ></div>
                      </div>
                    </div>
                  </div>
                  <div class="card-footer bg-transparent">
                    <div class="btn-group w-100" role="group">
                      <button 
                        class="btn btn-outline-primary btn-sm"
                        @click="editParkingLot(lot)"
                      >
                        <i class="fas fa-edit"></i>
                      </button>
                      <button 
                        class="btn btn-outline-info btn-sm"
                        @click="viewParkingLotDetails(lot)"
                      >
                        <i class="fas fa-eye"></i>
                      </button>
                      <button 
                        class="btn btn-outline-danger btn-sm"
                        @click="deleteParkingLot(lot)"
                        :disabled="!lot.is_empty"
                      >
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="parkingLots.length === 0" class="text-center py-5">
              <i class="fas fa-building fa-3x text-muted mb-3"></i>
              <h5 class="text-muted">No Parking Lots Found</h5>
              <p class="text-muted">Create your first parking lot to get started.</p>
              <button 
                class="btn btn-primary"
                data-bs-toggle="modal" 
                data-bs-target="#createParkingLotModal"
              >
                <i class="fas fa-plus me-1"></i>
                Add Parking Lot
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar with Recent Activity -->
      <div class="col-lg-4">
        <!-- Recent Users Accordion -->
        <div class="card shadow mb-4">
          <div class="card-header py-3">
            <h6 class="m-0 font-weight-bold text-primary">Recent Activity</h6>
          </div>
          <div class="card-body">
            <div class="accordion" id="activityAccordion">
              <!-- Recent Users -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button 
                    class="accordion-button" 
                    type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#recentUsers" 
                    aria-expanded="true" 
                    aria-controls="recentUsers"
                  >
                    <i class="fas fa-users me-2"></i>
                    Recent Registrations
                  </button>
                </h2>
                <div 
                  id="recentUsers" 
                  class="accordion-collapse collapse show" 
                  data-bs-parent="#activityAccordion"
                >
                  <div class="accordion-body">
                    <div v-for="user in recentUsers" :key="user.id" class="d-flex align-items-center mb-2">
                      <div class="flex-shrink-0">
                        <div class="avatar-circle bg-primary text-white">
                          {{ user.username.charAt(0).toUpperCase() }}
                        </div>
                      </div>
                      <div class="flex-grow-1 ms-3">
                        <div class="fw-bold">{{ user.username }}</div>
                        <small class="text-muted">{{ user.email }}</small>
                      </div>
                      <small class="text-muted">{{ formatDate(user.created_at) }}</small>
                    </div>
                  </div>
                </div>
              </div>

              <!-- System Stats -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button 
                    class="accordion-button collapsed" 
                    type="button" 
                    data-bs-toggle="collapse" 
                    data-bs-target="#systemStats" 
                    aria-expanded="false" 
                    aria-controls="systemStats"
                  >
                    <i class="fas fa-chart-bar me-2"></i>
                    System Statistics
                  </button>
                </h2>
                <div 
                  id="systemStats" 
                  class="accordion-collapse collapse" 
                  data-bs-parent="#activityAccordion"
                >
                  <div class="accordion-body">
                    <div class="mb-3">
                      <label class="form-label small text-muted">Occupancy Rate</label>
                      <div class="progress mb-1">
                        <div 
                          class="progress-bar bg-primary" 
                          :style="{ width: occupancyRate + '%' }"
                        ></div>
                      </div>
                      <small class="text-muted">{{ occupancyRate.toFixed(1) }}%</small>
                    </div>
                    
                    <div class="mb-3">
                      <label class="form-label small text-muted">Revenue Today</label>
                      <div class="h5 text-success">₹{{ stats.todayRevenue || 0 }}</div>
                    </div>
                    
                    <div>
                      <label class="form-label small text-muted">Popular Location</label>
                      <div class="fw-bold">{{ stats.popularLocation || 'N/A' }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Parking Lot Modal -->
    <CreateParkingLotModal @parking-lot-created="handleParkingLotCreated" />
    
    <!-- Edit Parking Lot Modal -->
    <EditParkingLotModal 
      v-if="selectedParkingLot"
      :parking-lot="selectedParkingLot"
      @parking-lot-updated="handleParkingLotUpdated"
      @modal-closed="selectedParkingLot = null"
    />
    
    <!-- Parking Lot Details Modal -->
    <ParkingLotDetailsModal 
      v-if="detailsParkingLot"
      :parking-lot="detailsParkingLot"
      @modal-closed="detailsParkingLot = null"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import CreateParkingLotModal from '../../components/admin/CreateParkingLotModal.vue'
// import EditParkingLotModal from '../../components/admin/EditParkingLotModal.vue'
// import ParkingLotDetailsModal from '../../components/admin/ParkingLotDetailsModal.vue'
import axios from 'axios'

const authStore = useAuthStore()

// Reactive data
const parkingLots = ref([])
const recentUsers = ref([])
const searchQuery = ref('')
const filterStatus = ref('')
const selectedParkingLot = ref(null)
const detailsParkingLot = ref(null)
const loading = ref(false)

const stats = reactive({
  totalLots: 0,
  availableSpots: 0,
  occupiedSpots: 0,
  totalUsers: 0,
  todayRevenue: 0,
  popularLocation: ''
})

// Computed properties
const filteredParkingLots = computed(() => {
  let filtered = parkingLots.value

  if (searchQuery.value) {
    filtered = filtered.filter(lot => 
      lot.prime_location_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      lot.address.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }

  if (filterStatus.value) {
    const isActive = filterStatus.value === 'active'
    filtered = filtered.filter(lot => lot.is_active === isActive)
  }

  return filtered
})

const occupancyRate = computed(() => {
  const total = stats.availableSpots + stats.occupiedSpots
  return total > 0 ? (stats.occupiedSpots / total) * 100 : 0
})

// Methods
const fetchParkingLots = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/admin/pkl/list')
    parkingLots.value = response.data.data || []
    calculateStats()
  } catch (error) {
    console.error('Error fetching parking lots:', error)
  } finally {
    loading.value = false
  }
}

const fetchRecentUsers = async () => {
  try {
    const response = await axios.get('/api/admin/users')
    recentUsers.value = (response.data.data || []).slice(0, 5)
    stats.totalUsers = response.data.data?.length || 0
  } catch (error) {
    console.error('Error fetching users:', error)
  }
}

const calculateStats = () => {
  stats.totalLots = parkingLots.value.length
  stats.availableSpots = parkingLots.value.reduce((sum, lot) => sum + (lot.available_spots || 0), 0)
  stats.occupiedSpots = parkingLots.value.reduce((sum, lot) => sum + ((lot.number_of_spots || 0) - (lot.available_spots || 0)), 0)
}

const editParkingLot = (lot) => {
  selectedParkingLot.value = { ...lot }
}

const viewParkingLotDetails = (lot) => {
  detailsParkingLot.value = lot
}

const deleteParkingLot = async (lot) => {
  if (!confirm(`Are you sure you want to delete "${lot.prime_location_name}"?`)) return
  
  try {
    await axios.delete(`/api/admin/pkl/delete/${lot.id}`)
    await fetchParkingLots()
  } catch (error) {
    alert(error.response?.data?.message || 'Error deleting parking lot')
  }
}

const handleParkingLotCreated = () => {
  fetchParkingLots()
}

const handleParkingLotUpdated = () => {
  fetchParkingLots()
  selectedParkingLot.value = null
}

const refreshParkingLots = () => {
  fetchParkingLots()
}

const exportData = () => {
  // Implement export functionality
  console.log('Export data functionality')
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

// Lifecycle
onMounted(() => {
  fetchParkingLots()
  fetchRecentUsers()
})
</script>

<style scoped>
.border-left-primary {
  border-left: 0.25rem solid var(--bs-primary) !important;
}

.border-left-success {
  border-left: 0.25rem solid var(--bs-success) !important;
}

.border-left-warning {
  border-left: 0.25rem solid var(--bs-warning) !important;
}

.border-left-info {
  border-left: 0.25rem solid var(--bs-info) !important;
}

.parking-lot-card {
  transition: transform 0.2s;
}

.parking-lot-card:hover {
  transform: translateY(-2px);
}

.spots-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(20px, 1fr));
  gap: 3px;
  max-height: 60px;
  overflow: hidden;
}

.spot-indicator {
  width: 20px;
  height: 20px;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.spot-indicator.available {
  background-color: var(--bs-success);
}

.spot-indicator.occupied {
  background-color: var(--bs-danger);
}

.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.accordion-button:not(.collapsed) {
  background-color: rgba(var(--bs-primary-rgb), 0.1);
  border-color: var(--bs-primary);
}
</style>
