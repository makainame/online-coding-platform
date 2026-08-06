<script setup>
import { onMounted, reactive, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import api from "../api";

const classes = ref([]);
const students = ref([]);
const loading = ref(false);
const saving = ref(false);
const createName = ref("");
const renameVisible = ref(false);
const renameForm = reactive({
  id: null,
  name: "",
});

async function loadAll() {
  loading.value = true;
  try {
    const [classResponse, studentResponse] = await Promise.all([
      api.get("/admin/classes"),
      api.get("/admin/students"),
    ]);
    classes.value = classResponse.data;
    students.value = studentResponse.data;
  } finally {
    loading.value = false;
  }
}

async function createClass() {
  const name = createName.value.trim();
  if (!name) {
    ElMessage.error("请输入班级名称");
    return;
  }
  saving.value = true;
  try {
    await api.post("/admin/classes", { name });
    createName.value = "";
    ElMessage.success("班级已创建");
    await loadAll();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "创建失败");
  } finally {
    saving.value = false;
  }
}

function openRename(item) {
  renameForm.id = item.id;
  renameForm.name = item.name;
  renameVisible.value = true;
}

async function renameClass() {
  const name = renameForm.name.trim();
  if (!name) {
    ElMessage.error("班级名称不能为空");
    return;
  }
  saving.value = true;
  try {
    await api.put(`/admin/classes/${renameForm.id}`, { name });
    renameVisible.value = false;
    ElMessage.success("班级已重命名");
    await loadAll();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "重命名失败");
  } finally {
    saving.value = false;
  }
}

async function deleteClass(item) {
  try {
    await ElMessageBox.confirm(
      `删除“${item.name}”后，该班学生将变为未分班。`,
      "删除班级",
      {
        type: "warning",
        confirmButtonText: "确认",
        cancelButtonText: "取消",
      },
    );
  } catch {
    return;
  }
  try {
    await api.delete(`/admin/classes/${item.id}`);
    ElMessage.success("班级已删除");
    await loadAll();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "删除失败");
  }
}

async function assignStudent(student, classId) {
  try {
    await api.put(`/admin/students/${student.id}/class`, {
      class_id: classId || null,
    });
    ElMessage.success("分班已保存");
    await loadAll();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "分班失败");
    await loadAll();
  }
}

onMounted(loadAll);
</script>

<template>
  <section class="page">
    <div class="page-head">
      <div>
        <h1>班级管理</h1>
        <p>{{ classes.length }} 个班级 · {{ students.length }} 个学生账号</p>
      </div>
      <div class="create-bar">
        <el-input
          v-model="createName"
          placeholder="新班级名称"
          clearable
          style="width: 220px"
          @keyup.enter="createClass"
        />
        <el-button type="primary" :loading="saving" @click="createClass">
          创建班级
        </el-button>
      </div>
    </div>

    <div class="panel">
      <h3 class="section-title">班级列表</h3>
      <el-table v-loading="loading" :data="classes" row-key="id">
        <el-table-column prop="id" label="#" width="80" />
        <el-table-column prop="name" label="班级名称" min-width="200" />
        <el-table-column prop="student_count" label="学生数" width="120" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button link type="primary" @click="openRename(row)">
              重命名
            </el-button>
            <el-button link type="danger" @click="deleteClass(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="!loading && classes.length === 0" class="empty-state">
        暂无班级，请先创建
      </div>
    </div>

    <div class="panel">
      <h3 class="section-title">学生分班</h3>
      <el-table v-loading="loading" :data="students" row-key="id">
        <el-table-column prop="id" label="#" width="80" />
        <el-table-column prop="username" label="用户名" min-width="160" />
        <el-table-column prop="email" label="邮箱" min-width="220" />
        <el-table-column label="所属班级" min-width="220">
          <template #default="{ row }">
            <el-select
              :model-value="row.class_id"
              placeholder="未分班"
              clearable
              style="width: 100%"
              @change="(value) => assignStudent(row, value)"
            >
              <el-option
                v-for="item in classes"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="!loading && students.length === 0" class="empty-state">
        暂无学生账号
      </div>
    </div>
  </section>

  <el-dialog v-model="renameVisible" title="重命名班级" width="420px">
    <el-form label-position="top">
      <el-form-item label="班级名称">
        <el-input v-model="renameForm.name" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="renameVisible = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="renameClass">
        保存
      </el-button>
    </template>
  </el-dialog>
</template>

<style scoped>
.create-bar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title {
  margin: 0 0 14px;
  font-size: 16px;
  color: #1f2937;
}
</style>
