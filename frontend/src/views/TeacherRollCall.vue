<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import * as XLSX from "xlsx";
import api from "../api";

const students = ref([]);
const loading = ref(false);
const saving = ref(false);
const importing = ref(false);
const classFilter = ref("");
const pickCount = ref(1);
const currentPicks = ref([]);
const pickedIds = ref(new Set());
const groups = ref([]);
const groupPickCount = ref(1);
const currentGroupPicks = ref([]);
const pickedGroupIds = ref(new Set());
const newGroupName = ref("");
const groupLoading = ref(false);
const groupSaving = ref(false);
const fileInput = ref(null);
const addVisible = ref(false);
const addForm = reactive({
  name: "",
  class_name: "",
});

const classOptions = computed(() => {
  const names = new Set(
    students.value
      .map((item) => item.class_name?.trim())
      .filter(Boolean),
  );
  return [...names].sort((a, b) => a.localeCompare(b, "zh-CN"));
});

const filteredStudents = computed(() => {
  if (!classFilter.value) return students.value;
  return students.value.filter((item) => item.class_name === classFilter.value);
});

const remainingCount = computed(
  () => filteredStudents.value.filter((item) => !pickedIds.value.has(item.id)).length,
);

async function loadStudents() {
  loading.value = true;
  try {
    const { data } = await api.get("/admin/roll-call/students");
    students.value = data;
  } finally {
    loading.value = false;
  }
}

async function loadGroups() {
  groupLoading.value = true;
  try {
    const { data } = await api.get("/admin/roll-call/groups");
    groups.value = data;
  } finally {
    groupLoading.value = false;
  }
}

function downloadTemplate() {
  const rows = [
    ["name", "class_name"],
    ["张三", "一班"],
    ["李四", "一班"],
    ["王五", "二班"],
  ];
  const worksheet = XLSX.utils.aoa_to_sheet(rows);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "点名名单");
  XLSX.writeFile(workbook, "随机点名导入模板.xlsx");
}

async function importStudents(payload) {
  importing.value = true;
  try {
    const { data } = await api.post("/admin/roll-call/students/import", payload);
    ElMessage.success(`导入完成：新增 ${data.created}，跳过 ${data.skipped}`);
    await loadStudents();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "导入失败");
  } finally {
    importing.value = false;
  }
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
          name: row.name || row["姓名"] || "",
          class_name: row.class_name || row["班级"] || row["班级名称"] || "",
        }))
        .filter((row) => row.name);
      if (payload.length === 0) {
        ElMessage.error("Excel 中没有有效的学生姓名");
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

function shuffle(items) {
  const result = [...items];
  for (let index = result.length - 1; index > 0; index -= 1) {
    const target = Math.floor(Math.random() * (index + 1));
    [result[index], result[target]] = [result[target], result[index]];
  }
  return result;
}

function randomPick() {
  let candidates = filteredStudents.value.filter(
    (item) => !pickedIds.value.has(item.id),
  );
  if (candidates.length === 0) {
    ElMessage.info("本轮名单已全部点过，已自动开始新一轮");
    pickedIds.value = new Set();
    candidates = [...filteredStudents.value];
  }
  if (candidates.length === 0) {
    ElMessage.warning("当前名单中没有学生");
    return;
  }
  const count = Math.min(pickCount.value, candidates.length);
  currentPicks.value = shuffle(candidates).slice(0, count);
  currentPicks.value.forEach((item) => {
    pickedIds.value.add(item.id);
  });
}

function resetPicked() {
  pickedIds.value = new Set();
  currentPicks.value = [];
  ElMessage.success("已重置本轮点名记录");
}

function randomGroupPick() {
  let candidates = groups.value.filter(
    (item) => !pickedGroupIds.value.has(item.id),
  );
  if (candidates.length === 0) {
    ElMessage.info("所有小组都已抽过，已自动开始新一轮");
    pickedGroupIds.value = new Set();
    candidates = [...groups.value];
  }
  if (candidates.length === 0) {
    ElMessage.warning("请先添加小组");
    return;
  }
  const count = Math.min(groupPickCount.value, candidates.length);
  currentGroupPicks.value = shuffle(candidates).slice(0, count);
  currentGroupPicks.value.forEach((item) => {
    pickedGroupIds.value.add(item.id);
  });
}

function resetGroupPicked() {
  pickedGroupIds.value = new Set();
  currentGroupPicks.value = [];
  ElMessage.success("已重置小组抽取记录");
}

async function addGroup() {
  const name = newGroupName.value.trim();
  if (!name) {
    ElMessage.error("请输入小组名称");
    return;
  }
  groupSaving.value = true;
  try {
    await api.post("/admin/roll-call/groups", { name });
    newGroupName.value = "";
    ElMessage.success("小组已添加");
    await loadGroups();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "添加小组失败");
  } finally {
    groupSaving.value = false;
  }
}

async function renameGroup(group) {
  let value = "";
  try {
    const result = await ElMessageBox.prompt("请输入新的小组名称", "重命名小组", {
      inputValue: group.name,
      confirmButtonText: "确认",
      cancelButtonText: "取消",
    });
    value = result.value?.trim() || "";
  } catch {
    return;
  }
  if (!value) {
    ElMessage.error("小组名称不能为空");
    return;
  }
  try {
    await api.put(`/admin/roll-call/groups/${group.id}`, { name: value });
    ElMessage.success("小组已重命名");
    await loadGroups();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "重命名失败");
  }
}

async function deleteGroup(group) {
  try {
    await ElMessageBox.confirm(
      `确定删除小组“${group.name}”吗？`,
      "删除小组",
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
    await api.delete(`/admin/roll-call/groups/${group.id}`);
    ElMessage.success("小组已删除");
    await loadGroups();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "删除小组失败");
  }
}

async function addStudent() {
  const name = addForm.name.trim();
  if (!name) {
    ElMessage.error("请输入学生姓名");
    return;
  }
  saving.value = true;
  try {
    await api.post("/admin/roll-call/students", {
      name,
      class_name: addForm.class_name.trim(),
    });
    addVisible.value = false;
    addForm.name = "";
    addForm.class_name = "";
    ElMessage.success("学生已加入点名名单");
    await loadStudents();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "添加失败");
  } finally {
    saving.value = false;
  }
}

async function deleteStudent(student) {
  try {
    await ElMessageBox.confirm(
      `确定从点名名单删除“${student.name}”吗？`,
      "删除学生",
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
    await api.delete(`/admin/roll-call/students/${student.id}`);
    ElMessage.success("已删除");
    await loadStudents();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "删除失败");
  }
}

async function clearAll() {
  try {
    await ElMessageBox.confirm(
      "确定清空整个点名名单吗？",
      "清空名单",
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
    await api.delete("/admin/roll-call/students");
    students.value = [];
    currentPicks.value = [];
    pickedIds.value = new Set();
    ElMessage.success("点名名单已清空");
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "清空失败");
  }
}

onMounted(() => {
  loadStudents();
  loadGroups();
});
</script>

<template>
  <section class="page">
    <div class="page-head">
      <div>
        <h1>随机点名</h1>
        <p>{{ students.length }} 个学生 · {{ classOptions.length }} 个班级</p>
      </div>
      <div class="head-actions">
        <el-button @click="downloadTemplate">下载模板</el-button>
        <el-button @click="fileInput?.click()">Excel 导入</el-button>
        <el-button type="primary" @click="addVisible = true">手动添加</el-button>
        <el-button type="danger" plain @click="clearAll">清空名单</el-button>
      </div>
      <input
        ref="fileInput"
        type="file"
        accept=".xlsx,.xls"
        class="hidden-input"
        @change="handleExcel"
      />
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <strong>{{ students.length }}</strong>
        <span>总名单</span>
      </div>
      <div class="stat-card">
        <strong>{{ classOptions.length }}</strong>
        <span>班级数</span>
      </div>
      <div class="stat-card">
        <strong>{{ pickedIds.size }}</strong>
        <span>本轮已点</span>
      </div>
      <div class="stat-card">
        <strong>{{ remainingCount }}</strong>
        <span>当前剩余</span>
      </div>
    </div>

    <div class="panel roll-controls">
      <div class="control-row">
        <el-select
          v-model="classFilter"
          placeholder="全部班级"
          clearable
          style="width: 180px"
        >
          <el-option
            v-for="item in classOptions"
            :key="item"
            :label="item"
            :value="item"
          />
        </el-select>
        <el-input-number
          v-model="pickCount"
          :min="1"
          :max="5"
          label="抽取人数"
        />
        <el-button type="primary" size="large" @click="randomPick">
          随机点名
        </el-button>
        <el-button size="large" @click="resetPicked">重置本轮</el-button>
      </div>
    </div>

    <div v-if="currentPicks.length" class="pick-result panel">
      <h3>本次抽中</h3>
      <div class="pick-grid">
        <div
          v-for="(item, index) in currentPicks"
          :key="item.id"
          class="pick-card"
        >
          <span class="pick-index">{{ index + 1 }}</span>
          <strong>{{ item.name }}</strong>
          <span>{{ item.class_name || "未分班" }}</span>
        </div>
      </div>
    </div>

    <div class="panel group-panel">
      <h3 class="section-title">小组随机抽取</h3>
      <div v-loading="groupLoading" class="group-list">
        <div
          v-for="group in groups"
          :key="group.id"
          class="group-chip"
          :class="{ picked: pickedGroupIds.has(group.id) }"
        >
          <span class="group-name">{{ group.name }}</span>
          <span class="group-status">
            {{ pickedGroupIds.has(group.id) ? "已抽" : "未抽" }}
          </span>
          <el-button link type="primary" @click="renameGroup(group)">
            重命名
          </el-button>
          <el-button link type="danger" @click="deleteGroup(group)">
            删除
          </el-button>
        </div>
      </div>

      <div class="control-row group-controls">
        <el-input
          v-model="newGroupName"
          placeholder="新小组名称"
          clearable
          style="width: 180px"
          @keyup.enter="addGroup"
        />
        <el-button :loading="groupSaving" @click="addGroup">添加小组</el-button>
        <el-input-number
          v-model="groupPickCount"
          :min="1"
          :max="Math.max(1, groups.length)"
          label="抽取组数"
        />
        <el-button type="primary" size="large" @click="randomGroupPick">
          随机抽组
        </el-button>
        <el-button size="large" @click="resetGroupPicked">重置小组</el-button>
      </div>

      <div v-if="currentGroupPicks.length" class="pick-result">
        <h3>本次抽中小组</h3>
        <div class="pick-grid">
          <div
            v-for="(group, index) in currentGroupPicks"
            :key="group.id"
            class="pick-card group-pick-card"
          >
            <span class="pick-index">{{ index + 1 }}</span>
            <strong>{{ group.name }}</strong>
          </div>
        </div>
      </div>
    </div>

    <div class="panel">
      <h3 class="section-title">点名名单</h3>
      <el-table v-loading="loading" :data="filteredStudents" row-key="id">
        <el-table-column type="index" label="#" width="80" :index="(index) => index + 1" />
        <el-table-column prop="name" label="姓名" min-width="160" />
        <el-table-column prop="class_name" label="班级" min-width="180">
          <template #default="{ row }">{{ row.class_name || "未分班" }}</template>
        </el-table-column>
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-tag
              :type="pickedIds.has(row.id) ? 'success' : 'info'"
              effect="plain"
            >
              {{ pickedIds.has(row.id) ? "已点" : "未点" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button link type="danger" @click="deleteStudent(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="!loading && filteredStudents.length === 0" class="empty-state">
        暂无名单，请先导入 Excel 或手动添加学生
      </div>
    </div>
  </section>

  <el-dialog v-model="addVisible" title="添加点名学生" width="420px">
    <el-form label-position="top">
      <el-form-item label="姓名">
        <el-input v-model="addForm.name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="班级">
        <el-input v-model="addForm.class_name" autocomplete="off" placeholder="可留空" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="addVisible = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="addStudent">
        添加
      </el-button>
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 14px;
}

.stat-card {
  min-height: 86px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 6px;
  padding: 14px;
  background: #ffffff;
  border: 1px solid #dde3e8;
  border-radius: 8px;
}

.stat-card strong {
  font-size: 24px;
  color: #176b5b;
}

.stat-card span {
  color: #64748b;
  font-size: 13px;
}

.roll-controls {
  margin-bottom: 14px;
}

.control-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.group-panel {
  margin-bottom: 14px;
}

.group-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 14px;
  min-height: 44px;
}

.group-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: 1px solid #dde3e8;
  border-radius: 8px;
  background: #ffffff;
}

.group-chip.picked {
  border-color: #16a34a;
  background: #f0fdf4;
}

.group-name {
  font-weight: 700;
  color: #1f2937;
}

.group-status {
  color: #64748b;
  font-size: 12px;
}

.group-controls {
  margin-top: 4px;
}

.group-pick-card strong {
  color: #176b5b;
}

.pick-result {
  margin-bottom: 14px;
}

.pick-result h3 {
  margin: 0 0 12px;
  font-size: 16px;
}

.pick-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
}

.pick-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 22px 16px;
  border: 1px solid #176b5b;
  border-radius: 8px;
  background: #f0f7f5;
}

.pick-card strong {
  font-size: 24px;
  color: #0f172a;
}

.pick-card span {
  color: #64748b;
}

.pick-index {
  position: absolute;
  top: 8px;
  left: 10px;
  color: #176b5b;
  font-weight: 700;
}

.section-title {
  margin: 0 0 14px;
  font-size: 16px;
  color: #1f2937;
}
</style>
