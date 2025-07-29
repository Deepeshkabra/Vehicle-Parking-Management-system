<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title">Parking Lots</h5>
          </div>
          <div class="card-body">
            <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addLotModal">
              Add New Lot
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bootstrap Modal -->
    <div class="modal fade" id="addLotModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Parking Lot</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label class="form-label">Location Name</label>
                <input type="text" class="form-control" v-model="locationName">
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const locationName = ref('')

// Bootstrap JS components can be used via CDN
onMounted(() => {
  // Example: Initialize tooltips
  const modal = new bootstrap.Modal(document.getElementById('myModal'))
  const tooltip = new bootstrap.Tooltip(document.getElementById('myTooltip'))
  const dropdown = new bootstrap.Dropdown(document.getElementById('myDropdown'))
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
})
</script>
