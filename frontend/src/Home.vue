<template>
  <div class="vpn-bg">
    <header>
      <nav class="navbar" aria-label="Main navigation">
        <router-link to="/" class="logo">VPN MOYASHIELD</router-link>
      
        <label for="nav-toggle" class="nav-toggle-label" aria-label="Abrir menú de navegación">
          <span></span>
        </label>
        <div class="nav-actions">
        </div>
      </nav>
    </header>

    <main class="home-container">
      
      <!-- 🔗 Sección promocional -->
      <section class="promo-section">
        <div class="promo-content">
          <div class="promo-left">
            <img src="/LOGO.png" alt="escudo vpn" class="promo-image" />
          </div>
          <div class="promo-right">
            <h1>NAVEGA DE FORMA SEGURA </h1>
            <ul class="features-list">
              <li>conexion por tunel a servidor </li>
              <li>Acceda libremente a contenidos globales</li>
              <li>Conexiones más rápidas y estables</li>
            </ul>
            <div class="highlights">
              <span>✔ ideal para empresas </span>
              <span>✔ facil uso </span>
              <span>✔ seguridad a red publicas</span>
              <span>✔ Servidor de confianza</span>
            </div>
            <div class="cta-buttons">
              <a href="#" class="btn">configurar </a>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
// Aquí puedes agregar la lógica de tu componente principal
</script>

<style scoped>
* {
  box-sizing: border-box;
}

html, body {
  margin: 0;
  padding: 0;
  background: linear-gradient(135deg, #23272f 0%, #181a20 100%);
  overflow-x: hidden;
  font-family: sans-serif;
}

.vpn-bg {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #23272f 0%, #181a20 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
}

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

.btn:hover {
  background: #00e6a8;
  color: #23272f;
}

.home-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  padding: 4rem 2rem;
  max-width: 1200px;
}

h1 {
  color: #00e6a8;
  margin-bottom: 1.5rem;
  font-size: 2.5rem;
  text-align: center;
}

p {
  color: #f3f0f0;
  font-size: 1.2rem;
  text-align: center;
  max-width: 600px;
}

.promo-section {
  width: 100%;
  padding: 4rem 2rem;
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
  display: flex;
  flex-direction: column;
  align-items: center;
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

/* Responsive */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .nav-links {
    flex-direction: column;
    width: 100%;
    display: none;
  }

  .nav-links.active {
    display: flex;
  }

  .nav-toggle-label {
    display: block;
    cursor: pointer;
    color: #00e6a8;
    font-size: 1.5rem;
  }

  .promo-content {
    flex-direction: column;
  }

  .cta-buttons {
    flex-direction: column;
  }
  .cta-buttons {
  display: flex;
  justify-content: center;
  width: 100%; /* Esto es clave para que el botón se pueda centrar */
  margin-top: 1rem;
}


}

</style>
