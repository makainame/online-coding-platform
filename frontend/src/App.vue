<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import {
  Cpu,
  Key,
  Link,
  Lock,
  Message,
  Picture,
  User,
} from "@element-plus/icons-vue";
import api from "./api";
import { pageLoading } from "./loading";

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

function switchAuth(mode) {
  authMode.value = mode;
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
    ElMessage.success(authMode.value === "login" ? "登录成功" : "注册成功");
    if (router.currentRoute.value.name === "home") {
      router.replace({ path: "/", query: { t: Date.now() } });
    } else {
      router.push("/");
    }
  } catch (error) {
    ElMessage.error(
      error.response?.data?.detail ||
        (authMode.value === "login" ? "登录失败" : "注册失败"),
    );
  } finally {
    loading.value = false;
  }
}

function logout() {
  localStorage.removeItem("token");
  user.value = null;
  router.push("/");
}

onMounted(async () => {
  pageLoading.value = true;
  await loadUser();
  pageLoading.value = false;
});
</script>

<template>
  <div v-if="pageLoading" class="page-loading">
    <div class="loading-spinner"></div>
    <span>加载中...</span>
  </div>

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
        <router-link v-if="user?.role === 'teacher'" to="/classes">
          班级管理
        </router-link>
        <router-link v-if="user?.role === 'teacher'" to="/admin/exams">
          考试管理
        </router-link>
        <router-link v-if="user?.role === 'teacher'" to="/question-bank">
          题库管理
        </router-link>
        <router-link v-if="user?.role === 'teacher'" to="/teacher-stats">
          统计面板
        </router-link>
        <router-link v-if="user?.role === 'student'" to="/exams">
          考试
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
      <router-view :key="$route.fullPath" />
    </main>
  </div>

  <el-dialog
    v-model="showAuth"
    width="460px"
    destroy-on-close
    class="auth-dialog"
  >
    <div class="auth-header">
      <h2>{{ authMode === "login" ? "欢迎回来" : "创建账号" }}</h2>
      <p>
        {{
          authMode === "login"
            ? "登录后继续练习、考试和查看学习记录"
            : "注册后即可开始在线练习"
        }}
      </p>
    </div>

    <div class="auth-tabs">
      <button
        type="button"
        :class="{ active: authMode === 'login' }"
        @click="switchAuth('login')"
      >
        登录
      </button>
      <button
        type="button"
        :class="{ active: authMode === 'register' }"
        @click="switchAuth('register')"
      >
        注册
      </button>
    </div>

    <el-form label-position="top" class="auth-form">
      <el-form-item label="用户名">
        <el-input
          v-model="form.username"
          :prefix-icon="User"
          autocomplete="username"
          placeholder="请输入用户名"
        />
      </el-form-item>
      <el-form-item label="密码">
        <el-input
          v-model="form.password"
          :prefix-icon="Lock"
          type="password"
          show-password
          autocomplete="current-password"
          placeholder="请输入密码"
        />
      </el-form-item>
      <template v-if="authMode === 'register'">
        <el-form-item label="邮箱">
          <el-input
            v-model="form.email"
            :prefix-icon="Message"
            autocomplete="email"
            placeholder="选填，用于找回账号"
          />
        </el-form-item>
        <el-form-item label="头像">
          <div class="avatar-upload">
            <label class="avatar-picker">
              <img
                v-if="avatarPreview"
                :src="avatarPreview"
                class="avatar-preview"
                alt=""
              />
              <span v-else class="avatar-placeholder">选择头像</span>
              <input
                type="file"
                accept="image/*"
                class="avatar-input"
                @change="onAvatarChange"
              />
            </label>
            <span class="avatar-tip">支持 jpg/png，不超过 2MB</span>
          </div>
        </el-form-item>
        <el-form-item label="角色">
          <el-radio-group v-model="form.role" class="auth-radio-group">
            <el-radio-button value="student">学生</el-radio-button>
            <el-radio-button value="teacher">教师</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <template v-if="form.role === 'student'">
          <el-form-item label="AI 服务商">
            <el-radio-group v-model="form.ai_provider" class="auth-radio-group">
              <el-radio-button value="deepseek">DeepSeek</el-radio-button>
              <el-radio-button value="qwen">通义千问</el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="API 地址">
            <el-input
              v-model="form.ai_base_url"
              :prefix-icon="Link"
              placeholder="API 地址"
            />
          </el-form-item>
          <el-form-item label="模型">
            <el-input
              v-model="form.ai_model"
              :prefix-icon="Cpu"
              placeholder="模型名称"
            />
          </el-form-item>
          <el-form-item label="自己的 API Key">
            <el-input
              v-model="form.ai_api_key"
              :prefix-icon="Key"
              type="password"
              show-password
              placeholder="输入自己的 API Key"
            />
          </el-form-item>
        </template>
        <template v-else>
          <el-form-item label="教师授权码">
            <el-input
              v-model="form.teacher_code"
              :prefix-icon="Key"
              type="password"
              show-password
              placeholder="请输入教师授权码"
            />
          </el-form-item>
        </template>
      </template>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <button
          class="text-button"
          type="button"
          @click="switchAuth(authMode === 'login' ? 'register' : 'login')"
        >
          {{ authMode === "login" ? "注册账号" : "已有账号" }}
        </button>
        <el-button
          type="primary"
          class="auth-submit"
          :loading="loading"
          @click="submitAuth"
        >
          {{ authMode === "login" ? "登录" : "注册" }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.page-loading {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 14px;
  background: rgba(244, 246, 248, 0.92);
  color: #475569;
  font-weight: 600;
}

.loading-spinner {
  width: 38px;
  height: 38px;
  border: 4px solid #dbe4e8;
  border-top-color: #176b5b;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

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

.auth-header {
  padding: 4px 2px 16px;
}

.auth-header h2 {
  margin: 0 0 6px;
  font-size: 22px;
  letter-spacing: 0;
}

.auth-header p {
  margin: 0;
  color: #64748b;
}

.auth-tabs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px;
  padding: 5px;
  margin-bottom: 18px;
  border-radius: 8px;
  background: #f1f4f6;
}

.auth-tabs button {
  height: 36px;
  border: 0;
  border-radius: 6px;
  background: transparent;
  color: #64748b;
  font-weight: 600;
  cursor: pointer;
}

.auth-tabs button.active {
  background: #ffffff;
  color: #176b5b;
  box-shadow: 0 1px 3px rgba(15, 23, 42, 0.1);
}

.auth-form :deep(.el-form-item) {
  margin-bottom: 16px;
}

.auth-radio-group {
  display: flex;
}

.avatar-picker {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 1px dashed #cbd5e1;
  background: #f8fafc;
  cursor: pointer;
  overflow: hidden;
}

.avatar-placeholder {
  color: #64748b;
  font-size: 12px;
  text-align: center;
}

.avatar-input {
  display: none;
}

.avatar-tip {
  color: #94a3b8;
  font-size: 12px;
}

.auth-submit {
  min-width: 108px;
}

.dialog-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}
</style>
