<template>
  <div class="vpn-bg">
    <header>
      <nav class="navbar" aria-label="Main navigation">
        <router-link to="/" class="logo">VPN MOYASHIELD</router-link>
        <input type="checkbox" id="nav-toggle" class="nav-toggle" />
        <label for="nav-toggle" class="nav-toggle-label" aria-label="Abrir menú de navegación">
          <span></span>
        </label>
        <ul class="nav-links">
          <li><a href="#" class="active">INFORMACION</a></li>
        </ul>
        <div class="nav-actions">
          <router-link to="/login">
            <button class="btn login">Iniciar sesión</button>
          </router-link>
          <router-link to="/register">
            <button class="btn register">Regístrate</button>
          </router-link>
        </div>
      </nav>
    </header>

    <main class="home-container">
      <h1>Bienvenido a VPN MOYASHIELD</h1>
      <p>Protege tu privacidad y navega seguro en cualquier red.</p>
      
      <section class="promo-section">
        <div class="promo-content">
          <div class="promo-left">
            <img src="/LOGO.png" alt="Persona usando smartphone" class="promo-image" />
          </div>
          <div class="promo-right">
            <h2>Accede a servidores de todo el mundo</h2>
            <ul class="features-list">
              <li>Servidores de alta velocidad para una conectividad global excepcional</li>
              <li>Acceda libremente a contenidos globales</li>
              <li>Conexiones más rápidas y estables</li>
            </ul>
            <div class="highlights">
              <span>✔ Vía de luz</span>
              <span>✔ 105 Países</span>
              <span>✔ 10 Gbps</span>
              <span>✔ Servidor de confianza</span>
            </div>
            
            <div class="cta-buttons vpn-control-area">
              <a href="#" class="btn">Servidores</a> 
              
              <button 
                @click="toggleVpn" 
                :disabled="loading" 
                :class="['btn', 'secondary', { 'btn-disconnect-style': isVpnConnected }]">
                
                <span v-if="loading">Cargando...</span>
                <span v-else>{{ isVpnConnected ? 'DESCONECTAR VPN' : 'CONECTAR VPN' }}</span>
              </button>
            </div>
            
            <div class="vpn-status-info">
                <span :class="['status-pill', statusTextClass]">{{ statusLabel }}</span>
                <p v-if="message" :class="statusMessageClass">{{ message }}</p>
            </div>
            </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios'; 


// Asegúrate de que el archivo .env tenga VITE_API_URL y VITE_API_KEY
const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8080';
const apiKey = import.meta.env.VITE_API_KEY || 'ClaveVPNUni2025';

// --- ESTADO REACTIVO ---
const isVpnConnected = ref(false); 
const loading = ref(false);        
const message = ref('');           
const status = ref('');            

// --- COMPUTADAS PARA CLASES Y TEXTO DINÁMICO ---

const statusTextClass = computed(() => {
    if (loading.value) return 'status-loading';
    return isVpnConnected.value ? 'status-active' : 'status-inactive';
});

const statusLabel = computed(() => {
    if (loading.value) return 'Cargando...';
    return isVpnConnected.value ? 'VPN ACTIVA' : 'VPN INACTIVA';
});

const statusMessageClass = computed(() => ({
    'text-success': status.value === 'success',
    'text-error': status.value === 'error',
}));

// --- MÉTODO PRINCIPAL DE TOGGLE ---

const toggleVpn = async () => {
    // 1. Determinar la acción (invertir el estado actual)
    const action = isVpnConnected.value ? 'deactivate' : 'activate';
    const endpoint = `${apiUrl}/${action}`;
    
    // 2. Actualizar estado de carga y mensajes
    loading.value = true;
    message.value = `Intentando ${action === 'activate' ? 'conectar' : 'desconectar'}...`;
    status.value = '';

    try {
        // 3. Petición POST a la API de Flask
        const response = await axios.post(endpoint, {}, {
            headers: {
                'X-API-Key': apiKey, // Clave para la autenticación
                'Content-Type': 'application/json',
            },
        });
        
        // 4. Manejar respuesta exitosa (código 200 OK)
        status.value = 'success';
        message.value = response.data.message;
        
        // 5. Actualizar el estado de conexión
        isVpnConnected.value = (action === 'activate'); 

    } catch (error) {
        // 6. Manejar errores
        status.value = 'error';
        isVpnConnected.value = false; // Asumimos desconexión o fallo

        if (error.response) {
            // Error de la API (ej: clave incorrecta, error de comando)
            message.value = `Error de API (${error.response.status}): ${error.response.data.message}`;
        } else {
            // Error de red (Flask no está corriendo)
            message.value = 'Error de red: Asegúrate de que el backend de Flask esté corriendo en http://127.0.0.1:8080.';
        }
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
/* Fondo general */
html,
body {
  margin: 0;
  padding: 0;
  background: linear-gradient(135deg, #23272f 0%, #181a20 100%);
  overflow-x: hidden;
}



.vpn-bg {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #23272f 0%, #181a20 100%);
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  align-items: center;
  
}

/* Navegación moderna y responsive */
.navbar {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 2rem;
  background: #23272f;
  box-shadow: 8px 8px 24px #181a20, -8px -8px 24px #2e323a;
  border-radius: 24px;
  margin-top: 2rem;
  position: relative;
  z-index: 10;
}
.logo {
  color: #00e6a8;
  font-size: clamp(1.2rem, 2vw, 2rem);
  font-weight: bold;
  letter-spacing: 1px;
}
.nav-links {
  list-style: none;
  display: flex;
  gap: clamp(1rem, 3vw, 2.5rem);
  margin: 0;
  padding: 0;
}
.nav-links a {
  color: #fff;
  text-decoration: none;
  font-size: clamp(1rem, 2vw, 1.2rem);
  transition: color 0.2s;
}
.nav-links a:hover {
  color: #00e6a8;
}
.nav-actions {
  display: flex;
  gap: 1rem;
}
.btn {
  padding: 0.5em 1.7em;
  border-radius: 20px;
  font-size: clamp(0.95rem, 2vw, 1.1rem);
  cursor: pointer;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  background: #23272f;
  color: #00e6a8;
  box-shadow: 6px 6px 16px #181a20, -6px -6px 16px #2e323a;
  border: 2px solid #00e6a8;
}
.btn.login:hover,
.btn.register:hover {
  background: #00e6a8;
  color: #23272f;
}

/* Toggle para menú móvil */
.nav-toggle,
.nav-toggle-label {
  display: none;
}

/* Contenido principal */
.home-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  padding: 4rem 2rem;
  box-sizing: border-box;
  z-index: 1;
}
h1 {
  color: #00e6a8;
  margin-bottom: 1.5rem;
  font-size: 2.5rem;
  text-align: center;
}
p {
  color: #bdbdbd;
  font-size: 1.2rem;
  text-align: center;
  max-width: 600px;
}

/* 🔗 Estilos para sección promocional */
.promo-section {
  width: 100%;
  padding: 4rem 2rem;
  box-sizing: border-box;
  background: #23272f;
  color: #ffffff;
}
.promo-content {
  display: flex;
  flex-wrap: wrap;
  max-width: 1200px;
  margin: auto;
  gap: 2rem;
  align-items: center;
}
.promo-left {
  flex: 1;
  text-align: center;
}
.promo-image {
  max-width: 100%;
  height: auto;
  border-radius: 24px;
  box-shadow: 6px 6px 16px #181a20, -6px -6px 16px #2e323a;
}
.promo-right {
  flex: 1;
}
.promo-right h2 {
  font-size: 2rem;
  color: #00e6a8;
  margin-bottom: 1.5rem;
}
.features-list {
  list-style: none;
  padding: 0;
  margin-bottom: 1.5rem;
}
.features-list li {
  margin-bottom: 0.75rem;
  font-size: 1.1rem;
  color: #bdbdbd;
}
.highlights {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 2rem;
}
.highlights span {
  background: #00e6a8;
  color: #23272f;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.95rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
.cta-buttons {
  display: flex;
  gap: 1rem;
}
.btn.secondary {
  background: #181a20;
  color: #00e6a8;
  border: 2px solid #00e6a8;
}
.btn.secondary:hover {
  background: #00e6a8;
  color: #23272f;
}

/* Contenedor del botón y estado */
.vpn-control-area {
    /* Asegura que el botón se ajuste al grid de los CTA */
    width: 100%;
    margin-bottom: 1rem;
}

/* Estilo para el botón cuando está en estado de DESCONEXIÓN */
.btn.secondary.btn-disconnect-style {
    /* Usamos tu color rojo/fondo para un estilo neumórfico de desconexión */
    background: #4d0000; 
    color: #ff4d4d; 
    border: 2px solid #ff4d4d; 
    box-shadow: 6px 6px 16px #181a20, -6px -6px 16px #2e323a;
}

.btn.secondary.btn-disconnect-style:hover:not(:disabled) {
    background: #ff4d4d;
    color: #23272f; /* Fondo de tus colores */
}

/* Estilos del indicador de estado */
.vpn-status-info {
    margin-top: 1rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
}

.status-pill {
    padding: 0.4rem 1rem;
    border-radius: 15px;
    font-weight: bold;
    font-size: 0.9rem;
    transition: var(--transicion-media);
}

.status-active {
    background-color: var(--color-acento); /* Verde acento */
    color: var(--color-fondo-principal);
    box-shadow: 0 4px 8px rgba(0, 230, 168, 0.5);
}

.status-inactive {
    background-color: #4d4d4d;
    color: #181a20;
    box-shadow: 0 4px 8px rgba(255, 77, 77, 0.3);
}

.status-loading {
    background-color: #6c5ce7; /* Morado para carga */
    color: white;
}

.text-success { color: var(--color-acento); font-weight: bold; }
.text-error { color: #ff4d4d; font-weight: bold; }

</style>
