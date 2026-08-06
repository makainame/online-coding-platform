<script setup>
import { onMounted, reactive, ref } from "vue";
import { ElMessage } from "element-plus";
import * as XLSX from "xlsx";
import api from "../api";

const students = ref([]);
const loading = ref(false);
const saving = ref(false);
const createVisible = ref(false);
const importVisible = ref(false);
const resetVisible = ref(false);
const currentStudent = ref(null);
const fileInput = ref(null);
const importing = ref(false);
const importJson = ref(`[
  {
    "username": "student01",
    "password": "123456",
    "email": "student01@example.com",
    "ai_api_key": ""
  },
  {
    "username": "student02",
    "password": "123456",
    "email": "student02@example.com",
    "ai_api_key": ""
  }
]`);
const createForm = reactive({
  username: "",
  password: "",
  email: "",
});
const resetForm = reactive({
  password: "",
});

async function loadStudents() {
  loading.value = true;
  try {
    const { data } = await api.get("/admin/students");
    students.value = data;
  } finally {
    loading.value = false;
  }
}

async function createStudent() {
  saving.value = true;
  try {
    await api.post("/admin/students", { ...createForm });
    createVisible.value = false;
    createForm.username = "";
    createForm.password = "";
    createForm.email = "";
    await loadStudents();
  } finally {
    saving.value = false;
  }
}

async function importStudents(payload = null) {
  importing.value = true;
  if (payload === null) {
    try {
      payload = JSON.parse(importJson.value);
    } catch (error) {
      ElMessage.error(`JSON 格式错误：${error.message}`);
      importing.value = false;
      return;
    }
  }
  if (!Array.isArray(payload) || payload.length === 0) {
    ElMessage.error("学生数据必须是非空数组");
    importing.value = false;
    return;
  }
  try {
    const { data } = await api.post("/admin/students/import", payload);
    ElMessage.success(`导入完成：新增 ${data.created}，跳过 ${data.skipped}`);
    importVisible.value = false;
    await loadStudents();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "导入失败");
  } finally {
    importing.value = false;
  }
}

function downloadTemplate() {
  const rows = [
    ["username", "password", "email", "ai_api_key"],
    ["student01", "123456", "student01@example.com", ""],
    ["student02", "123456", "student02@example.com", ""],
  ];
  const worksheet = XLSX.utils.aoa_to_sheet(rows);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "学生");
  XLSX.writeFile(workbook, "学生导入模板.xlsx");
}

function handleExcel(event) {
  const file = event.target.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    try {
      const data = new Uint8Array(e.target.result);
      const workbook = XLSX.read(data, { type: "array" });
      const sheet = workbook.Sheets[workbook.SheetNames[0]];
      const rows = XLSX.utils.sheet_to_json(sheet, { defval: "" });
      const payload = rows
        .map((row) => ({
          username: row.username || row["用户名"],
          password: row.password || row["密码"],
          email: row.email || row["邮箱"] || "",
          ai_api_key:
            row.ai_api_key || row["AI API Key"] || row["AI Key"] || "",
        }))
        .filter((row) => row.username && row.password);
      if (payload.length === 0) {
        ElMessage.error("Excel 中没有有效学生数据");
        return;
      }
      importStudents(payload);
    } catch (error) {
      ElMessage.error(`Excel 解析失败：${error.message}`);
    } finally {
      event.target.value = "";
    }
  };
  reader.readAsArrayBuffer(file);
}

function openReset(student) {
  currentStudent.value = student;
  resetForm.password = "";
  resetVisible.value = true;
}

async function resetPassword() {
  saving.value = true;
  try {
    await api.put(`/admin/students/${currentStudent.value.id}/password`, {
      password: resetForm.password,
    });
    resetVisible.value = false;
    await loadStudents();
  } finally {
    saving.value = false;
  }
}

function formatTime(value) {
  return value ? new Date(value).toLocaleString() : "-";
}

onMounted(loadStudents);
</script>

<template>
  <section class="page">
    <div class="page-head">
      <div>
        <h1>学生管理</h1>
        <p>{{ students.length }} 个学生账号</p>
      </div>
      <div class="head-actions">
        <el-button @click="downloadTemplate">下载模板</el-button>
        <el-button @click="fileInput?.click()">Excel 导入</el-button>
        <el-button @click="importVisible = true">批量导入</el-button>
        <el-button type="primary" @click="createVisible = true">创建学生</el-button>
      </div>
      <input
        ref="fileInput"
        type="file"
        accept=".xlsx,.xls"
        class="hidden-input"
        @change="handleExcel"
      />
    </div>

    <div class="panel">
      <el-table v-loading="loading" :data="students" row-key="id">
        <el-table-column prop="id" label="#" width="80" />
        <el-table-column prop="username" label="用户名" min-width="140" />
        <el-table-column prop="class_name" label="班级" min-width="120">
          <template #default="{ row }">{{ row.class_name || "未分班" }}</template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column label="创建时间" min-width="180">
          <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
        </el-table-column>
        <el-table-column prop="submission_count" label="提交数" width="100" />
        <el-table-column prop="accepted_count" label="通过数" width="100" />
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button link type="primary" @click="openReset(row)">重置密码</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="!loading && students.length === 0" class="empty-state">
        暂无学生账号
      </div>
    </div>
  </section>

  <el-dialog v-model="createVisible" title="创建学生账号" width="420px">
    <el-form label-position="top">
      <el-form-item label="用户名">
        <el-input v-model="createForm.username" autocomplete="off" />
      </el-form-item>
      <el-form-item label="初始密码">
        <el-input v-model="createForm.password" type="password" show-password />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="createForm.email" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="createVisible = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="createStudent">创建</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="importVisible" title="批量导入学生" width="680px">
    <el-input
      v-model="importJson"
      type="textarea"
      :rows="14"
      class="json-input"
    />
    <template #footer>
      <el-button @click="importVisible = false">取消</el-button>
      <el-button type="primary" :loading="importing" @click="importStudents">
        导入
      </el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="resetVisible" title="重置密码" width="420px">
    <p>为 {{ currentStudent?.username }} 设置新密码</p>
    <el-form label-position="top">
      <el-form-item label="新密码">
        <el-input v-model="resetForm.password" type="password" show-password />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="resetVisible = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="resetPassword">保存</el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.head-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.hidden-input {
  display: none;
}

.json-input {
  font-family: "Cascadia Code", Consolas, monospace;
}
</style>
