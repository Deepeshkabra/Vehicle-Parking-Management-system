<template>
  <div class="container-fluid py-4">
    <!-- Header with Navigation -->
    <div class="row mb-4">
      <div class="col-12">
        <div class="card shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h3 class="text-primary mb-1">Welcome to User Dashboard</h3>
                <p class="text-muted mb-0">{{ authStore.user?.username || 'User' }}</p>
              </div>
              <div class="btn-group">
                <router-link to="/user/dashboard" class="btn btn-outline-primary btn-sm">Home</router-link>
                <router-link to="/user/profile" class="btn btn-outline-info btn-sm">Profile</router-link>
                <button @click="authStore.logout()" class="btn btn-outline-danger btn-sm">Logout</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Left Column - Recent History & Search -->
      <div class="col-lg-8">
        <!-- Recent Parking History Accordion -->
        <div class="accordion mb-4" id="userAccordion">
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button 
                class="accordion-button" 
                type="button" 
                data-bs-toggle="collapse" 
                data-bs-target="#recentHistory" 
                aria-expanded="true"
              >
                <i class="fas fa-history me-2"></i>
                Recent Parking History
              </button>
            </h2>
            <div id="recentHistory" class="accordion-collapse collapse show" data-bs-parent="#userAccordion">
              <div class="accordion-body">
                <div class="table-responsive">
                  <table class="table table-hover">
                    <thead class="table-light">
                      <tr>
                        <th>ID</th>
                        <th>Location</th>
                        <th>Vehicle No</th>
                        <th>Timestamp</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="booking in recentBookings" :key="booking.id">
                        <td>{{ booking.id }}</td>
                        <td>{{ booking.location || 'N/A' }}</td>
                        <td>{{ booking.vehicle_number }}</td>
                        <td>{{ formatDateTime(booking.parking_timestamp) }}</td>
                        <td>
                          <button 
                            v-if="booking.status === 'active'"
                            @click="openReleaseModal(booking)"
                            class="btn btn-warning btn-sm"
                          >
                            Release
                          </button>
                          <span v-else class="badge bg-success">Completed</span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>

          <!-- Search Parking Lots -->
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button 
                class="accordion-button collapsed" 
                type="button" 
                data-bs-toggle="collapse" 
                data-bs-target="#searchParking"
              >
                <i class="fas fa-search me-2"></i>
                Search Parking Lots
              </button>
            </h2>
            <div id="searchParking" class="accordion-collapse collapse" data-bs-parent="#userAccordion">
              <div class="accordion-body">
                <div class="row mb-3">
                  <div class="col-md-8">
                    <div class="input-group">
                      <input 
                        type="text" 
                        class="form-control" 
                        placeholder="Search by location or pin code..."
                        v-model="searchQuery"
                      >
                      <button class="btn btn-primary" @click="searchParkingLots">
                        <i class="fas fa-search"></i>
                      </button>
                    </div>
                  </div>
                </div>
                
                <!-- Search Results -->
                <div v-if="searchResults.length > 0">
                  <h6 class="text-primary mb-3">Parking Lots @ {{ searchQuery || 'All Locations' }}</h6>
                  <div class="table-responsive">
                    <table class="table table-striped">
                      <thead class="table-primary">
                        <tr>
                          <th>ID</th>
                          <th>Address</th>
                          <th>Availability</th>
                          <th>Price</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="lot in searchResults" :key="lot.id">
                          <td>{{ lot.id }}</td>
                          <td>{{ lot.address }}</td>
                          <td>
                            <span class="badge bg-success">{{ lot.available_spots || 0 }}</span>
                            / {{ lot.number_of_spots || 0 }}
                          </td>
                          <td>₹{{ lot.price }}/hr</td>
                          <td>
                            <button 
                              @click="openBookingModal(lot)"
                              class="btn btn-primary btn-sm"
                              :disabled="!lot.available_spots"
                            >
                              Book
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column - Quick Stats -->
      <div class="col-lg-4">
        <div class="card shadow mb-4">
          <div class="card-header bg-primary text-white">
            <h6 class="mb-0">Quick Stats</h6>
          </div>
          <div class="card-body">
            <div class="row text-center">
              <div class="col-6 mb-3">
                <h4 class="text-primary">{{ userStats.totalBookings }}</h4>
                <small class="text-muted">Total Bookings</small>
              </div>
              <div class="col-6 mb-3">
                <h4 class="text-success">{{ userStats.activeBookings }}</h4>
                <small class="text-muted">Active</small>
              </div>
            </div>
          </div>
        </div>
        <ParkingHistory />
      </div>
    </div>

    <!-- Booking Modal -->
    <BookingModal 
      v-if="selectedLot"
      :parking-lot="selectedLot"
      @booking-confirmed="handleBookingConfirmed"
      @modal-closed="selectedLot = null"
    />

    <!-- Release Modal -->
    <ReleaseModal 
      v-if="selectedBooking"
      :booking="selectedBooking"
      @release-confirmed="handleReleaseConfirmed"
      @modal-closed="selectedBooking = null"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import BookingModal from '@/components/user/BookingModal.vue'
import ReleaseModal from '@/components/user/ReleaseModal.vue'
import ParkingHistory from '@/components/user/parkingHistory.vue'

const authStore = useAuthStore()

// Reactive data
const recentBookings = ref([])
const searchQuery = ref('')
const searchResults = ref([])
const selectedLot = ref(null)
const selectedBooking = ref(null)

const userStats = reactive({
  totalBookings: 0,
  activeBookings: 0
})

// Methods
const fetchRecentBookings = async () => {
  try {
    const response = await axios.get('/api/user/pkl/book/list')
    recentBookings.value = response.data.data || []
    userStats.totalBookings = recentBookings.value.length
    userStats.activeBookings = recentBookings.value.filter(b => b.status === 'active').length
  } catch (error) {
    console.error('Error fetching bookings:', error)
  }
}

const searchParkingLots = async () => {
  try {
    const response = await axios.get('/api/user/pkl/list')
    let lots = response.data.data || []
    
    if (searchQuery.value) {
      lots = lots.filter(lot => 
        lot.prime_location_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        lot.address.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
        lot.pin_code.includes(searchQuery.value)
      )
    }
    
    searchResults.value = lots
  } catch (error) {
    console.error('Error searching parking lots:', error)
  }
}

const openBookingModal = (lot) => {
  selectedLot.value = lot
}

const openReleaseModal = (booking) => {
  selectedBooking.value = booking
}

const handleBookingConfirmed = () => {
  selectedLot.value = null
  fetchRecentBookings()
  searchParkingLots()
}

const handleReleaseConfirmed = () => {
  selectedBooking.value = null
  fetchRecentBookings()
}

const formatDateTime = (dateString) => {
  return new Date(dateString).toLocaleString()
}

onMounted(() => {
  fetchRecentBookings()
  searchParkingLots()
})
</script>
