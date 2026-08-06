import { createRouter, createWebHistory } from "vue-router";
import { startPageLoading, stopPageLoading } from "./loading";
import AdminExams from "./views/AdminExams.vue";
import AiSettings from "./views/AiSettings.vue";
import Classes from "./views/Classes.vue";
import ExamTaking from "./views/ExamTaking.vue";
import Home from "./views/Home.vue";
import Problem from "./views/Problem.vue";
import QuestionBank from "./views/QuestionBank.vue";
import StudentExams from "./views/StudentExams.vue";
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
    { path: "/classes", name: "classes", component: Classes },
    { path: "/exams", name: "exams", component: StudentExams },
    { path: "/exam/:id", name: "exam-taking", component: ExamTaking },
    { path: "/admin/exams", name: "admin-exams", component: AdminExams },
    { path: "/question-bank", name: "question-bank", component: QuestionBank },
    { path: "/teacher-stats", name: "teacher-stats", component: TeacherStats },
    { path: "/ai-settings", name: "ai-settings", component: AiSettings },
  ],
});

router.beforeEach(() => {
  startPageLoading();
});

router.afterEach(() => {
  setTimeout(stopPageLoading, 60);
});

router.onError(() => {
  stopPageLoading();
});

export default router;
