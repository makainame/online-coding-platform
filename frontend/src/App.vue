<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import api from "./api";

const router = useRouter();
const user = ref(null);
const showAuth = ref(false);
const authMode = ref("login");
const loading = ref(false);
const form = reactive({
  username: "student",
  password: "student123",
  email: "",
  role: "student",
  ai_provider: "deepseek",
  ai_base_url: "https://api.deepseek.com/v1",
  ai_model: "deepseek-v4-flash",
  ai_api_key: "",
  teacher_code: "",
  avatar_base64: "",
});
const avatarPreview = ref("");

const AI_PRESETS = {
  deepseek: {
    base_url: "https://api.deepseek.com/v1",
    model: "deepseek-v4-flash",
  },
  qwen: {
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    model: "qwen3.7-plus",
  },
};

watch(
  () => form.ai_provider,
  (provider) => {
    const preset = AI_PRESETS[provider] || AI_PRESETS.deepseek;
    form.ai_base_url = preset.base_url;
    form.ai_model = preset.model;
  }
);

async function loadUser() {
  const token = localStorage.getItem("token");
  if (!token) return;
  try {
    const { data } = await api.get("/users/me");
    user.value = data;
  } catch {
    localStorage.removeItem("token");
    user.value = null;
  }
}

function onAvatarChange(event) {
  const file = event.target.files?.[0];
  if (!file) return;
  if (!file.type.startsWith("image/")) {
    ElMessage.error("请选择图片文件");
    event.target.value = "";
    return;
  }
  if (file.size > 2 * 1024 * 1024) {
    ElMessage.error("头像不能超过 2MB");
    event.target.value = "";
    return;
  }
  const reader = new FileReader();
  reader.onload = (e) => {
    avatarPreview.value = e.target.result;
    form.avatar_base64 = e.target.result;
  };
  reader.readAsDataURL(file);
  event.target.value = "";
}

function openAuth(mode = "login") {
  authMode.value = mode;
  showAuth.value = true;
}

async function submitAuth() {
  loading.value = true;
  try {
    const path = authMode.value === "login" ? "/auth/login" : "/auth/register";
    const payload =
      authMode.value === "login"
        ? { username: form.username, password: form.password }
        : { ...form };
    const { data } = await api.post(path, payload);
    localStorage.setItem("token", data.token);
    user.value = data.user;
    showAuth.value = false;
    if (router.currentRoute.value.name === "home") {
      router.go(0);
    }
  } finally {
    loading.value = false;
  }
}

function logout() {
  localStorage.removeItem("token");
  user.value = null;
  router.push("/");
}

onMounted(loadUser);
</script>

<template>
  <div class="app-shell">
    <header class="topbar">
      <div class="brand">
        <span class="brand-mark">CP</span>
        <span class="brand-name">CodePractice</span>
      </div>
      <nav class="nav">
        <router-link to="/">题库</router-link>
        <router-link to="/submissions">提交记录</router-link>
        <router-link v-if="user?.role === 'teacher'" to="/students">
          学生管理
        </router-link>
        <router-link v-if="user?.role === 'teacher'" to="/question-bank">
          题库管理
        </router-link>
        <router-link v-if="user?.role === 'teacher'" to="/teacher-stats">
          统计面板
        </router-link>
        <router-link v-if="user" to="/ai-settings">AI 配置</router-link>
      </nav>
      <div class="user-area">
        <template v-if="user">
          <div class="avatar-wrap">
            <img v-if="user.avatar" :src="user.avatar" class="user-avatar" alt="" />
            <span v-else class="avatar-fallback">{{ (user.username || "U")[0].toUpperCase() }}</span>
          </div>
          <span class="user-chip">{{ user.username }}</span>
          <span class="role-chip" :class="user.role">
            {{ user.role === "teacher" ? "教师" : "学生" }}
          </span>
          <button class="text-button" type="button" @click="logout">退出</button>
        </template>
        <template v-else>
          <button class="primary-button" type="button" @click="openAuth('login')">登录</button>
          <button class="text-button" type="button" @click="openAuth('register')">注册</button>
        </template>
      </div>
    </header>

    <main class="main-content">
      <router-view />
    </main>
  </div>

  <el-dialog
    v-model="showAuth"
    :title="authMode === 'login' ? '登录' : '注册'"
    width="380px"
    destroy-on-close
  >
    <el-form label-position="top">
      <el-form-item label="用户名">
        <el-input v-model="form.username" autocomplete="username" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" type="password" show-password autocomplete="current-password" />
      </el-form-item>
      <template v-if="authMode === 'register'">
        <el-form-item label="邮箱">
          <el-input v-model="form.email" autocomplete="email" />
        </el-form-item>
        <el-form-item label="头像">
          <div class="avatar-upload">
            <img v-if="avatarPreview" :src="avatarPreview" class="avatar-preview" alt="" />
            <input type="file" accept="image/*" @change="onAvatarChange" />
          </div>
        </el-form-item>
        <el-form-item label="角色">
          <el-radio-group v-model="form.role">
            <el-radio value="student">学生</el-radio>
            <el-radio value="teacher">教师</el-radio>
          </el-radio-group>
        </el-form-item>
        <template v-if="form.role === 'student'">
          <el-form-item label="AI 服务商">
            <el-radio-group v-model="form.ai_provider">
              <el-radio value="deepseek">DeepSeek</el-radio>
              <el-radio value="qwen">通义千问</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="API 地址">
            <el-input v-model="form.ai_base_url" />
          </el-form-item>
          <el-form-item label="模型">
            <el-input v-model="form.ai_model" />
          </el-form-item>
          <el-form-item label="自己的 API Key">
            <el-input v-model="form.ai_api_key" type="password" show-password />
          </el-form-item>
        </template>
        <template v-else>
          <el-form-item label="教师授权码">
            <el-input v-model="form.teacher_code" type="password" show-password />
          </el-form-item>
        </template>
      </template>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <button
          class="text-button"
          type="button"
          @click="authMode = authMode === 'login' ? 'register' : 'login'"
        >
          {{ authMode === "login" ? "注册账号" : "已有账号" }}
        </button>
        <el-button type="primary" :loading="loading" @click="submitAuth">
          {{ authMode === "login" ? "登录" : "注册" }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.avatar-wrap {
  width: 32px;
  height: 32px;
  flex: 0 0 32px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-fallback {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #176b5b;
  color: #ffffff;
  font-size: 14px;
  font-weight: 700;
  user-select: none;
}

.avatar-upload {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-preview {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid #dde3e8;
}
</style>
