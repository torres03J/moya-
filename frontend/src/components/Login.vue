<template>
  <div class="login-bg">
    <header>
      <nav class="navbar">
        <router-link to="/" class="logo">VPN App</router-link>
        <ul class="nav-links">
          <li><router-link to="/">Inicio</router-link></li>
          <li><router-link to="/login">Login</router-link></li>
          <li><router-link to="/register">Registro</router-link></li>
        </ul>
      </nav>
    </header>

    <div class="login-container">
      <h2>Iniciar sesión</h2>
      <form>
        <div class="input-group">
          <label for="email">Correo electrónico</label>
          <input id="email" type="email" placeholder="Ingresa tu correo" required />
        </div>
        <div class="input-group">
          <label for="password">Contraseña</label>
          <input id="password" type="password" placeholder="Ingresa tu contraseña" required />
        </div>
        <button type="submit" class="btn-login">Entrar</button>
      </form>
      <router-link to="/register" class="login-link">¿No tienes cuenta? Regístrate</router-link>
    </div>
  </div>
</template>

<script setup>
// Script vacío para comenzar
</script>

<style scoped>
/* ====== RESET GLOBAL ====== */

/* ====== Fondo general ====== */
.login-bg {
   position: fixed;
  top: 0;
  left: 0;
  min-height: 100vh;
  width: 100vw;
  background: #23272f;
  display: flex;
  flex-direction: column;
}

/* ====== NAVBAR ====== */
.navbar {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.2rem 1rem;
  background: #23272f;
  box-shadow: 6px 6px 16px #181a20, -6px -6px 16px #2e323a;
  border-radius: 0 0 20px 20px;
  margin-bottom: 2rem;
}

.logo {
  font-size: 1.3rem;
  font-weight: bold;
  color: #00e6a8;
  text-decoration: none;
  margin-right: 2.5rem;
}

.nav-links {
  display: flex;
  gap: 2rem;
  list-style: none;
}

.nav-links a {
  color: #fff;
  text-decoration: none;
  font-size: 1.1rem;
  padding: 0.5rem 1.2rem;
  border-radius: 12px;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
}

.nav-links a:hover {
  background: #181a20;
  color: #00e6a8;
  box-shadow: 2px 2px 8px #181a20, -2px -2px 8px #2e323a;
}

/* ====== LOGIN CONTAINER ====== */
.login-container {
  flex: 1; 
  display: flex;
  flex-direction: column;
  justify-content: center; 
  align-items: center;     
  padding: 2rem;
}

.login-container h2 {
  color: #fff;
  margin-bottom: 1.5rem;
}

/* ====== FORM ====== */
form {
  width: 100%;
  max-width: 400px;
  background: #2e323a;
  padding: 2rem;
  border-radius: 18px;
  box-shadow: 4px 4px 12px #181a20, -4px -4px 12px #2e323a;
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

/* ====== BOTÓN ====== */
.btn-login {
  margin-top: 1rem;
  padding: 0.8rem;
  background: #00e6a8;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: bold;
  color: #23272f;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-login:hover {
  background: #00c792;
}

/* ====== LINK ====== */
.login-link {
  margin-top: 1rem;
  color: #00e6a8;
  text-decoration: underline;
  font-size: 0.95rem;
}
</style>
