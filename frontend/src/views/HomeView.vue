<script setup>
</script>

<template>
  <main class="landing-container">
    <h1 class="landing-title">Invitaciones Digitales</h1>
    <p class="landing-subtitle">Selecciona una invitación para ver la demostración</p>
    
    <div class="cards-container">
      <a href="/boda/demo-boda" class="card-link">
        <div class="card">
          <img 
            src="https://images.unsplash.com/photo-1519741497674-611481863552?w=400&h=300&fit=crop" 
            alt="Boda" 
            class="card-image"
          />
          <div class="card-content">
            <h2>Boda</h2>
            <span class="card-tag">Demo</span>
          </div>
        </div>
      </a>

      <a href="/15/15-feli" class="card-link">
        <div class="card">
          <img 
            src="https://images.unsplash.com/photo-1530103862676-de8c9debad1d?w=400&h=300&fit=crop" 
            alt="Quinceañera" 
            class="card-image"
          />
          <div class="card-content">
            <h2>Quince años</h2>
            <span class="card-tag">Demo</span>
          </div>
        </div>
      </a>
    </div>

    <p class="construction-text">Web en construcción...</p>
  </main>
</template>

<style scoped>
.landing-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  font-family: Arial, sans-serif;
}

.landing-title {
  color: white;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.landing-subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.2rem;
  margin-bottom: 3rem;
}

.cards-container {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
  justify-content: center;
}

.card-link {
  text-decoration: none;
  display: block;
}

.card {
  width: 280px;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.card-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.card-content {
  padding: 1.5rem;
  text-align: center;
}

.card-content h2 {
  color: #333;
  font-size: 1.3rem;
  margin: 0 0 0.5rem 0;
}

.card-tag {
  display: inline-block;
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: bold;
}

.construction-text {
  margin-top: 3rem;
  color: rgba(255, 255, 255, 0.7);
  font-size: 1rem;
  font-style: italic;
}
</style>
