import { createRouter, createWebHistory } from "vue-router";
import AiSettings from "./views/AiSettings.vue";
import Home from "./views/Home.vue";
import Problem from "./views/Problem.vue";
import QuestionBank from "./views/QuestionBank.vue";
import Students from "./views/Students.vue";
import Submissions from "./views/Submissions.vue";
import TeacherStats from "./views/TeacherStats.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "home", component: Home },
    { path: "/problem/:id", name: "problem", component: Problem },
    { path: "/submissions", name: "submissions", component: Submissions },
    { path: "/students", name: "students", component: Students },
    { path: "/question-bank", name: "question-bank", component: QuestionBank },
    { path: "/teacher-stats", name: "teacher-stats", component: TeacherStats },
    { path: "/ai-settings", name: "ai-settings", component: AiSettings },
  ],
});

export default router;
