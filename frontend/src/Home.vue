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
          <li><a href="#" class="active">informacion</a></li>
          
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
    </main>
  </div>
</template>

<script setup>
// Aquí puedes agregar la lógica de tu componente principal
</script>

<style scoped>
 
/* Fondo general */
.vpn-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  min-height: 100vh;
  min-width: 100vw;
  background: linear-gradient(135deg, #23272f 0%, #181a20 100%);
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  align-items: center;
  z-index: 0;
}

/* Navegación moderna y responsive */
.navbar {
  width: 100vw;
  max-width: 100vw;
  min-width: 100vw;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 2rem;
  background: #23272f;
  box-shadow: 8px 8px 24px #181a20, -8px -8px 24px #2e323a;
  border-radius: 24px;
  position: relative;
  z-index: 10;
  min-height: 60px;
  box-sizing: border-box;
  margin-top: 2rem;
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
.nav-links a.active,
.nav-links a:hover {
  color: #00e6a8;
}
.nav-actions {
  display: flex;
  gap: 1rem;
}
.btn {
  padding: 0.5em 1.7em;
  border: none;
  border-radius: 20px;
  font-size: clamp(0.95rem, 2vw, 1.1rem);
  cursor: pointer;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
  outline: none;
  background: #23272f;
  color: #00e6a8;
  box-shadow: 6px 6px 16px #181a20, -6px -6px 16px #2e323a;
  border: 2px solid #00e6a8;
}
.btn.login,
.btn.register {
  background: #23272f;
  color: #00e6a8;
  border: 2px solid #00e6a8;
}
.btn.login:hover,
.btn.login:focus,
.btn.register:hover,
.btn.register:focus {
  background: #00e6a8;
  color: #23272f;
  border-color: #00e6a8;
}

/* Toggle para menú móvil */
.nav-toggle {
  display: none;
}
.nav-toggle-label {
  display: none;
  flex-direction: column;
  cursor: pointer;
  width: 32px;
  height: 32px;
  justify-content: center;
}
.nav-toggle-label span,
.nav-toggle-label span::before,
.nav-toggle-label span::after {
  display: block;
  background: #00e6a8;
  height: 4px;
  width: 100%;
  border-radius: 2px;
  position: relative;
  transition: all 0.3s;
}
.nav-toggle-label span::before,
.nav-toggle-label span::after {
  content: '';
  position: absolute;
}
.nav-toggle-label span::before {
  top: -10px;
}
.nav-toggle-label span::after {
  top: 10px;
}

@media (max-width: 1200px) {
  .navbar {
    padding: 1.2rem 1vw;
  }
}

@media (max-width: 900px) {
  .navbar {
    flex-wrap: wrap;
    padding: 1rem 2vw;
  }
  .nav-links {
    gap: 1rem;
  }
}

@media (max-width: 700px) {
  .nav-links,
  .nav-actions {
    display: none;
  }
  .nav-toggle-label {
    display: flex;
    margin-left: auto;
  }
  .nav-toggle:checked ~ .nav-links,
  .nav-toggle:checked ~ .nav-actions {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 60px;
    left: 0;
    width: 100vw;
    background: #23272f;
    padding: 1.5rem 0;
    z-index: 9;
    align-items: center;
    gap: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  }
  .nav-toggle:checked ~ .nav-actions {
    top: 120px;
  }
  .logo {
    font-size: 1.3rem;
  }
}

/* Contenido principal */
.home-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 0;
  width: 100vw;
  height: 100vh;
  box-sizing: border-box;
  padding: 4rem 0 2rem 0;
  z-index: 1;
  /* Neumorfismo sutil para el área principal */
  /* box-shadow: 12px 12px 32px #181a20, -12px -12px 32px #2e323a; */
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
</style>
