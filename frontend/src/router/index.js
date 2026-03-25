import { createRouter, createWebHistory } from 'vue-router';
import InvitationView from '../views/InvitationView.vue';
import HomeView from '../views/HomeView.vue';
import Login from '../views/Login.vue';
import AdminLayout from '../layouts/AdminLayout.vue';
import Clientes from '../views/Clientes.vue';
import Templates from '../views/Templates.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // --- Rutas Públicas ---
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/:tipo_evento/:slug',
      name: 'invitation',
      component: InvitationView,
    },

    // --- Rutas de Administración ---
    {
      path: '/admin/login',
      name: 'login',
      component: Login,
    },
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: '/admin/clientes' // Redirigir /admin a /admin/clientes
        },
        {
          path: 'clientes',
          name: 'admin-clientes',
          component: Clientes
        },
        {
          path: 'templates',
          name: 'admin-templates',
          component: Templates
        }
      ]
    },
  ],
});

// Guardia de navegación para proteger rutas de admin
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('isAuthenticated') === 'true';

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next('/admin/login');
    } else {
      next();
    }
  } else if (to.name === 'login' && isAuthenticated) {
    next('/admin/clientes');
  } else {
    next();
  }
});

export default router;
