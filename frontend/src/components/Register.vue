<template>
  <div class="vpn-bg">
    <header>
      <nav class="navbar" aria-label="Main navigation">
        <!-- LOGO -->
        <router-link to="/" class="logo">VPN MOYASHIELD</router-link>

        <!-- Checkbox Toggle -->
        <input type="checkbox" id="nav-toggle" class="nav-toggle" />
        <label for="nav-toggle" class="nav-toggle-label" aria-label="Abrir menú de navegación">
          <span></span>
        </label>

        <!-- LINKS -->
        <ul class="nav-links">
        </ul>

        <!-- BOTONES -->
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

    <!-- CONTENIDO REGISTRO -->
    <main class="register-container">
      <h2>Crear cuenta</h2>
      <form>
        <div class="input-group">
          <label for="nombre">Nombre</label>
          <input id="nombre" type="text" placeholder="Ingresa tu nombre" required />
        </div>
        <div class="input-group">
          <label for="apellido">Apellido</label>
          <input id="apellido" type="text" placeholder="Ingresa tu apellido" required />
        </div>
        <div class="input-group">
          <label for="usuario">Usuario</label>
          <input id="usuario" type="text" placeholder="Crea un nombre de usuario" required />
        </div>
        <div class="input-group">
          <label for="email">Correo electrónico</label>
          <input id="email" type="email" placeholder="Ingresa tu correo" required />
        </div>
        <div class="input-group">
          <label for="password">Contraseña</label>
          <input id="password" type="password" placeholder="Crea una contraseña" required />
        </div>
        <div class="input-group">
          <label for="confirm-password">Repetir contraseña</label>
          <input id="confirm-password" type="password" placeholder="Repite tu contraseña" required />
        </div>
        <button type="submit" class="btn submit">Registrarse</button>
      </form>
      <router-link to="/login" class="register-link">
        ¿Ya tienes cuenta? Inicia sesión
      </router-link>
    </main>
  </div>
</template>

<script setup>
// Aquí puedes agregar la lógica de tu registro (validaciones, envío al backend, etc.)
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
  background: linear-gradient(135deg, #23272f 0%, #181a20 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;
  z-index: 0;
}

/* ===== NAVBAR ===== */
.navbar {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 2rem;
  background: #23272f;
  box-shadow: 8px 8px 24px #181a20, -8px -8px 24px #2e323a;
  border-radius: 24px;
  position: relative;
  margin-top: 2rem;
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
}
.btn.login:hover,
.btn.register:hover {
  background: #00e6a8;
  color: #23272f;
}

/* Toggle móvil */
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

/* ===== REGISTER CONTAINER ===== */
.register-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  width: 100%;
  max-width: 500px;
  margin: auto;
}
.register-container h2 {
  color: #00e6a8;
  margin-bottom: 1.5rem;
}
form {
  background: #2e323a;
  padding: 2rem;
  border-radius: 18px;
  box-shadow: 6px 6px 16px #181a20, -6px -6px 16px #2e323a;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.input-group {
  display: flex;
  flex-direction: column;
}
label {
  color: #bdbdbd;
  margin-bottom: 0.5rem;
}
input {
  padding: 0.8rem;
  border-radius: 12px;
  border: none;
  outline: none;
  background: #23272f;
  color: #fff;
}
input::placeholder {
  color: #aaa;
}
.btn.submit {
  margin-top: 1rem;
  padding: 0.8rem;
  background: #00e6a8;
  color: #23272f;
  font-weight: bold;
  border-radius: 12px;
  border: none;
}
.btn.submit:hover {
  background: #00c792;
}
.register-link {
  margin-top: 1rem;
  color: #00e6a8;
  text-decoration: underline;
  font-size: 0.95rem;
  text-align: center;
}

/* ===== RESPONSIVE ===== */
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
    align-items: center;
    gap: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  }
  .nav-toggle:checked ~ .nav-actions {
    top: 140px;
  }
}
</style>

