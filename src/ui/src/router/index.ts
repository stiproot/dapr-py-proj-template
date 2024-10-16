import { createRouter, createWebHistory } from "vue-router";
import { AuthService } from "@/services/auth.service";

import ProjRootView from "../views/ProjRootView.vue";
import LandingView from "../views/LandingView.vue";
import ProjManagerView from "../views/ProjManagerView.vue";
import ProjHomeView from "../views/ProjHomeView.vue";
import ProjDefinitionView from "../views/ProjDefinitionView.vue";
import ProjEditInfoView from "../views/ProjEditInfoView.vue";
import SettingsView from "../views/SettingsView.vue";
import ProcManagerComponent from "../components/ProcManagerComponent.vue";
import LoginView from "../views/LoginView.vue";
import AuthCallbackView from "../views/AuthCallbackView.vue";

const authService = new AuthService();

const routes = [
  {
    path: "/",
    redirect: { name: "projects" },
  },
  {
    path: "/",
    name: "landing",
    component: LandingView,
    meta: { requiresAuth: true, title: "tmpl", description: "Welcome to Proxima, your Causal AI management tool." },
    children: [
      {
        path: "/projects",
        name: "projects",
        component: ProjManagerView,
        meta: { requiresAuth: true, title: "Projects | tmpl", description: "Manage your projects here." },
      },
      {
        path: "/projects/:projectId",
        name: "project",
        component: ProjRootView,
        props: (route: any) => ({ tabId: route.query["tab"] }),
        meta: { requiresAuth: true, title: "Project Details | tmpl", description: "View and manage project details." },
        children: [
          {
            path: "definition",
            name: "project.definition",
            component: ProjDefinitionView,
            props: (route: any) => ({ tabId: route.query["tab"] }),
            meta: { title: "Project Definition | tmpl", description: "Define project details." },
          }
        ],
      },
      {
        path: "/projects/:projectId/home",
        name: "project.home",
        component: ProjHomeView,
        meta: { title: "Project Home | tmpl", description: "Project home dashboard." },
      },
      {
        path: "/projects/:projectId/edit",
        name: "project.edit",
        component: ProjEditInfoView,
        meta: { title: "Edit Project | tmpl", description: "Edit project details." },
      },
      {
        path: "/projects/new",
        name: "definition",
        component: ProjDefinitionView,
        props: (route: any) => ({ tabId: route.query["tab"] }),
        meta: { requiresAuth: true, title: "New Project | tmpl", description: "Create a new project." },
      },
      {
        path: "/settings",
        name: "settings",
        component: SettingsView,
        meta: { requiresAuth: true, title: "Settings | tmpl", description: "Manage application settings." },
      },
      {
        path: "/processes",
        name: "processes",
        component: ProcManagerComponent,
        meta: { requiresAuth: true, title: "Processes | tmpl", description: "Manage processes." },
      },
    ]
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { requiresAuth: false, title: "Login | tmpl", description: "Login to your account." },
  },
  {
    path: "/authorization-code/callback",
    name: "callback",
    component: AuthCallbackView,
    meta: { requiresAuth: false, title: "tmpl", description: "Authorization callback." },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (authService.isAuthenticated()) {
      const accessToken = authService.getAccessToken();
      if (!accessToken) {
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        });
      }

      const expiry = accessToken?.obj.expiresAt * 1000;

      if (Date.now() > expiry) {
        console.info('router -> refreshing.');
        await authService.refreshTokens();
      }

      next();
    } else {
      console.info('router -> [NOT] authenticated.');
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      });
    }
  }
  else {
    console.info('router -> [NO] auth required. from: ', from, ', to: ', to, ' , next: ', next);
    next();
  }
});

router.afterEach((to) => {
  // Use the title from the meta field if it exists
  if (to.meta.title) {
    document.title = to.meta.title as string;
  }
});

export default router;