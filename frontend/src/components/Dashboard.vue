<template>
  <div class="dashboard-container">
    <h2>Panel VPN</h2>
    <p>Estado de la VPN: <strong>{{ vpnStatus }}</strong></p>
    <button @click="toggleVPN">
      {{ vpnStatus === 'activa' ? 'Desactivar VPN' : 'Activar VPN' }}
    </button>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      vpnStatus: 'inactiva' // Simulación inicial
    };
  },
  methods: {
    toggleVPN() {
      // Aquí se hará la petición al backend
      this.vpnStatus = this.vpnStatus === 'activa' ? 'inactiva' : 'activa';
    }
  }
};
</script>

<style scoped>
.dashboard-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background: #fff;
}
button {
  margin-top: 1rem;
}
</style>
