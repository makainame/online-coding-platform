<script setup>
import { computed, onMounted, reactive, ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import * as XLSX from "xlsx";
import api from "../api";

const exams = ref([]);
const problems = ref([]);
const classes = ref([]);
const loading = ref(false);
const saving = ref(false);
const autoLoading = ref(false);
const dialogVisible = ref(false);
const resultVisible = ref(false);
const results = ref([]);
const resultExam = ref(null);
const resultLoading = ref(false);
const exporting = ref(false);
const previewVisible = ref(false);
const previewData = ref(null);
const previewLoading = ref(false);
const editId = ref(null);
const activeStep = ref(0);
const stageOptions = [
  { value: "stage1", label: "Python 阶段一（Day01-Day03）" },
  { value: "stage2", label: "Python 阶段二（Day04-Day05）" },
  { value: "stage3", label: "Python 阶段三（Day06-Day08）" },
  { value: "advanced", label: "Python 进阶综合（进阶Day01-Day08）" },
  { value: "case", label: "Python 综合案例检测" },
];
const form = reactive({
  title: "",
  description: "",
  duration_minutes: 60,
  class_id: null,
  status: "draft",
  selectionMode: "auto",
  stage: "stage1",
  target_count: 10,
  problem_ids: [],
  knowledge_points: [],
  count_per_point: 3,
  difficulty: "all",
  language: "python",
});

const tagOptions = computed(() => {
  const tags = new Set();
  for (const item of problems.value) {
    for (const tag of (item.tags || "").split(",")) {
      const trimmed = tag.trim();
      if (trimmed) tags.add(trimmed);
    }
  }
  return [...tags].sort((a, b) => a.localeCompare(b, "zh-CN"));
});

const groupedTags = computed(() => {
  const groups = new Map();
  for (const tag of tagOptions.value) {
    let group = "其他知识点";
    if (/^(进阶)?Day\d+$/.test(tag)) {
      group = "教学进度";
    } else if (
      [
        "入门",
        "变量",
        "运算",
        "输出",
        "条件判断",
        "比较",
        "取余",
        "循环",
        "列表",
        "字符串",
        "字典",
        "集合",
        "元组",
        "函数",
        "递归",
        "类",
        "异常",
        "文件",
        "生成器",
        "装饰器",
        "functools",
        "itertools",
        "lambda",
        "推导式",
        "排序",
        "查找",
      ].includes(tag)
    ) {
      group = "Python 核心语法";
    } else if (["Python", "JavaScript", "Java", "C++"].includes(tag)) {
      group = "语言";
    }
    if (!groups.has(group)) groups.set(group, []);
    groups.get(group).push(tag);
  }
  const priority = ["教学进度", "Python 核心语法", "语言", "其他知识点"];
  return [...groups.entries()]
    .sort(
      (a, b) =>
        priority.indexOf(a[0]) - priority.indexOf(b[0]) ||
        a[0].localeCompare(b[0], "zh-CN"),
    )
    .map(([label, items]) => ({ label, items }));
});

const statusLabel = {
  draft: "草稿",
  published: "已发布",
  closed: "已关闭",
};

const statusType = {
  draft: "info",
  published: "success",
  closed: "danger",
};

async function loadAll() {
  loading.value = true;
  try {
    const [examResponse, problemResponse, classResponse] = await Promise.all([
      api.get("/admin/exams"),
      api.get("/problems"),
      api.get("/admin/classes"),
    ]);
    exams.value = examResponse.data;
    problems.value = problemResponse.data;
    classes.value = classResponse.data;
  } finally {
    loading.value = false;
  }
}

function resetForm() {
  form.title = "";
  form.description = "";
  form.duration_minutes = 60;
  form.class_id = null;
  form.status = "draft";
  form.selectionMode = "auto";
  form.stage = "stage1";
  form.target_count = 10;
  form.problem_ids = [];
  form.knowledge_points = [];
  form.count_per_point = 3;
  form.difficulty = "all";
  form.language = "python";
}

function openCreate() {
  editId.value = null;
  activeStep.value = 0;
  resetForm();
  dialogVisible.value = true;
}

async function openEdit(row) {
  editId.value = row.id;
  activeStep.value = 0;
  resetForm();
  try {
    const { data } = await api.get(`/admin/exams/${row.id}`);
    form.title = data.title;
    form.description = data.description;
    form.duration_minutes = data.duration_minutes;
    form.class_id = data.class_id;
    form.status = data.status;
    form.selectionMode = "manual";
    form.problem_ids = data.problems.map((item) => item.problem_id);
    dialogVisible.value = true;
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "加载考试失败");
  }
}

async function saveExam() {
  if (!validateTitle()) {
    return;
  }
  if (form.selectionMode !== "stage") {
    if (form.selectionMode === "auto" && form.problem_ids.length === 0) {
      ElMessage.error("请先点击自动选题");
      return;
    }
    if (form.problem_ids.length === 0) {
      ElMessage.error("请至少选择一道题目");
      return;
    }
  }
  saving.value = true;
  try {
    const payload =
      form.selectionMode === "stage"
        ? {
            title: form.title,
            description: form.description,
            duration_minutes: form.duration_minutes,
            class_id: form.class_id,
            status: form.status,
            stage: form.stage,
            target_count: form.target_count,
            language: "python",
          }
        : { ...form };
    let savedId = editId.value;
    if (editId.value) {
      await api.put(`/admin/exams/${editId.value}`, payload);
      ElMessage.success("考试已更新");
    } else {
      const path =
        form.selectionMode === "stage" ? "/admin/exams/stage" : "/admin/exams";
      const { data } = await api.post(path, payload);
      savedId = data.id;
      ElMessage.success("考试已创建");
    }
    dialogVisible.value = false;
    await loadAll();
    await previewById(savedId);
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "保存失败");
  } finally {
    saving.value = false;
  }
}

async function previewById(examId) {
  previewVisible.value = true;
  previewLoading.value = true;
  previewData.value = null;
  try {
    const { data } = await api.get(`/admin/exams/${examId}`);
    previewData.value = data;
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "加载预览失败");
    previewVisible.value = false;
  } finally {
    previewLoading.value = false;
  }
}

function openPreview(row) {
  previewById(row.id);
}

async function autoSelect() {
  if (!form.knowledge_points.length) {
    ElMessage.error("请先选择知识点");
    return;
  }
  autoLoading.value = true;
  try {
    const payload = {
      knowledge_points: form.knowledge_points,
      count_per_point: form.count_per_point,
      difficulty: form.difficulty,
      language: form.language,
    };
    const { data } = await api.post("/admin/exams/preview", payload);
    form.problem_ids = data.problem_ids;
    ElMessage.success(`已自动选出 ${data.problem_ids.length} 道题`);
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "自动选题失败");
  } finally {
    autoLoading.value = false;
  }
}

async function deleteExam(row) {
  try {
    await ElMessageBox.confirm(`确定删除考试“${row.title}”吗？`, "删除考试", {
      type: "warning",
    });
  } catch {
    return;
  }
  try {
    await api.delete(`/admin/exams/${row.id}`);
    ElMessage.success("考试已删除");
    await loadAll();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "删除失败");
  }
}

async function toggleStatus(row) {
  const nextStatus = row.status === "published" ? "closed" : "published";
  try {
    await api.put(`/admin/exams/${row.id}`, { status: nextStatus });
    ElMessage.success(nextStatus === "published" ? "考试已发布" : "考试已关闭");
    await loadAll();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "状态切换失败");
  }
}

async function showResults(row) {
  resultVisible.value = true;
  resultLoading.value = true;
  results.value = [];
  resultExam.value = null;
  try {
    const [examResponse, resultResponse] = await Promise.all([
      api.get(`/admin/exams/${row.id}`),
      api.get(`/admin/exams/${row.id}/results`),
    ]);
    resultExam.value = examResponse.data;
    results.value = resultResponse.data;
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "加载成绩失败");
  } finally {
    resultLoading.value = false;
  }
}

async function exportResults() {
  if (!resultExam.value || results.value.length === 0) {
    ElMessage.warning("暂无成绩可导出");
    return;
  }
  exporting.value = true;
  try {
    const problems = resultExam.value.problems || [];
    const headers = [
      "用户名",
      "班级",
      "邮箱",
      "状态",
      "得分",
      "通过题数",
      "总题数",
      "开始时间",
      "提交时间",
      ...problems.map(
        (problem) =>
          `${problem.title} (${problem.language})`,
      ),
    ];
    const rows = results.value.map((row) => [
      row.username,
      row.class_name || "",
      row.email || "",
      row.status,
      row.score ?? "",
      row.accepted_problems,
      row.total_problems,
      formatTime(row.started_at),
      formatTime(row.submitted_at),
      ...problems.map(
        (problem) =>
          ({
            accepted: "通过",
            submitted: "已提交",
            "": "未作答",
          })[row.problem_statuses?.[String(problem.problem_id)]] || "未作答",
      ),
    ]);
    const worksheet = XLSX.utils.aoa_to_sheet([headers, ...rows]);
    worksheet["!cols"] = [
      { wch: 16 },
      { wch: 16 },
      { wch: 26 },
      { wch: 12 },
      { wch: 10 },
      { wch: 10 },
      { wch: 10 },
      { wch: 20 },
      { wch: 20 },
      ...problems.map(() => ({ wch: 24 })),
    ];
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "考试成绩");
    const date = new Date().toISOString().slice(0, 10);
    const safeTitle = String(resultExam.value.title).replace(/[\\/:*?"<>|]/g, "_");
    XLSX.writeFile(workbook, `考试成绩_${safeTitle}_${date}.xlsx`);
    ElMessage.success("成绩已导出");
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "导出失败");
  } finally {
    exporting.value = false;
  }
}

function formatTime(value) {
  return value ? new Date(value).toLocaleString() : "-";
}

function validateTitle() {
  const title = form.title.trim();
  if (title.length < 2 || !/[\u4e00-\u9fa5A-Za-z]/.test(title)) {
    ElMessage.error("考试标题不能是纯数字或太短，请填写有意义的名称");
    return false;
  }
  return true;
}

function nextStep() {
  if (!validateTitle()) {
    return;
  }
  activeStep.value = 1;
}

function problemTitle(problemId) {
  return (
    problems.value.find((item) => item.id === problemId)?.title ||
    `题目 ${problemId}`
  );
}

onMounted(loadAll);
</script>

<template>
  <section class="page">
    <div class="page-head">
      <div>
        <h1>考试管理</h1>
        <p>{{ exams.length }} 场考试</p>
      </div>
      <el-button type="primary" @click="openCreate">新建考试</el-button>
    </div>

    <div class="panel">
      <el-table v-loading="loading" :data="exams" row-key="id">
        <el-table-column prop="id" label="#" width="80" />
        <el-table-column prop="title" label="考试名称" min-width="220" />
        <el-table-column label="班级" min-width="120">
          <template #default="{ row }">{{ row.class_name || "全体学生" }}</template>
        </el-table-column>
        <el-table-column label="状态" width="110">
          <template #default="{ row }">
            <el-tag :type="statusType[row.status]" effect="plain">
              {{ statusLabel[row.status] || row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="duration_minutes" label="时长(分钟)" width="120" />
        <el-table-column prop="problem_count" label="题数" width="90" />
        <el-table-column prop="attempt_count" label="参与人数" width="110" />
        <el-table-column label="创建时间" min-width="180">
          <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" min-width="260" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="openPreview(row)">预览</el-button>
            <el-button link type="primary" @click="openEdit(row)">编辑</el-button>
            <el-button link type="primary" @click="showResults(row)">成绩</el-button>
            <el-button link type="warning" @click="toggleStatus(row)">
              {{ row.status === "published" ? "关闭" : "发布" }}
            </el-button>
            <el-button link type="danger" @click="deleteExam(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="!loading && exams.length === 0" class="empty-state">
        暂无考试，请先创建
      </div>
    </div>
  </section>

  <el-dialog
    v-model="dialogVisible"
    :title="editId ? '编辑考试' : '新建考试'"
    width="760px"
  >
    <el-steps
      :active="activeStep"
      align-center
      finish-status="success"
      class="dialog-steps"
    >
      <el-step title="基本信息" />
      <el-step title="组卷方式" />
    </el-steps>

    <el-form label-position="top">
      <template v-if="activeStep === 0">
        <el-form-item label="考试名称">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="考试说明">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <div class="form-grid">
          <el-form-item label="时长(分钟)">
            <el-input-number v-model="form.duration_minutes" :min="1" :max="600" />
          </el-form-item>
          <el-form-item label="面向班级">
            <el-select v-model="form.class_id" clearable placeholder="全体学生">
              <el-option
                v-for="item in classes"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="form.status">
              <el-option label="草稿" value="draft" />
              <el-option label="已发布" value="published" />
              <el-option label="已关闭" value="closed" />
            </el-select>
          </el-form-item>
        </div>
      </template>

      <template v-else>
        <el-form-item label="组卷方式">
          <el-radio-group v-model="form.selectionMode">
            <el-radio-button value="stage">标准阶段卷</el-radio-button>
            <el-radio-button value="auto">知识点自动组卷</el-radio-button>
            <el-radio-button value="manual">手动选题</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="form.selectionMode === 'manual'" label="考试题目">
          <el-select
            v-model="form.problem_ids"
            multiple
            filterable
            placeholder="选择题目"
            style="width: 100%"
          >
            <el-option
              v-for="item in problems"
              :key="item.id"
              :label="`${item.title} (${item.language})`"
              :value="item.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item v-else-if="form.selectionMode === 'stage'" label="标准阶段卷">
          <div class="auto-form">
            <div class="auto-field">
              <span class="field-label">阶段模板</span>
              <el-select v-model="form.stage" style="width: 100%">
                <el-option
                  v-for="item in stageOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </div>
            <div class="auto-options stage-options">
              <div class="auto-field">
                <span class="field-label">目标题数</span>
                <el-input-number v-model="form.target_count" :min="5" :max="30" />
              </div>
            </div>
          </div>
          <div class="selected-block">
            <span class="selected-count">满分 100 分；按阶段知识点覆盖，难度比例 60% 基础 / 30% 标准 / 10% 拔高</span>
          </div>
        </el-form-item>

        <el-form-item v-else label="自动组卷">
          <div class="auto-form">
            <div class="auto-field">
              <span class="field-label">知识点</span>
              <el-select
                v-model="form.knowledge_points"
                multiple
                filterable
                collapse-tags
                collapse-tags-tooltip
                :max-collapse-tags="2"
                placeholder="选择知识点"
                style="width: 100%"
              >
                <el-option-group
                  v-for="group in groupedTags"
                  :key="group.label"
                  :label="group.label"
                >
                  <el-option
                    v-for="tag in group.items"
                    :key="tag"
                    :label="tag"
                    :value="tag"
                  />
                </el-option-group>
              </el-select>
            </div>
            <div class="auto-options">
              <div class="auto-field">
                <span class="field-label">每个知识点题数</span>
                <el-input-number
                  v-model="form.count_per_point"
                  :min="1"
                  :max="30"
                />
              </div>
              <div class="auto-field">
                <span class="field-label">难度</span>
                <el-select v-model="form.difficulty" style="width: 100%">
                  <el-option label="全部难度" value="all" />
                  <el-option label="简单" value="easy" />
                  <el-option label="中等" value="medium" />
                  <el-option label="困难" value="hard" />
                </el-select>
              </div>
              <div class="auto-field">
                <span class="field-label">语言</span>
                <el-select v-model="form.language" style="width: 100%">
                  <el-option label="Python" value="python" />
                  <el-option label="JavaScript" value="javascript" />
                  <el-option label="Java" value="java" />
                  <el-option label="C++" value="cpp" />
                </el-select>
              </div>
              <div class="auto-field">
                <span class="field-label">&nbsp;</span>
                <el-button :loading="autoLoading" @click="autoSelect">
                  自动选题
                </el-button>
              </div>
            </div>
          </div>
          <div v-if="form.problem_ids.length" class="selected-block">
            <span class="selected-count">已选 {{ form.problem_ids.length }} 道题</span>
            <div class="selected-tags">
              <el-tag
                v-for="problemId in form.problem_ids"
                :key="problemId"
                type="info"
                effect="plain"
              >
                {{ problemTitle(problemId) }}
              </el-tag>
            </div>
          </div>
        </el-form-item>
      </template>
    </el-form>
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button v-if="activeStep === 1" @click="activeStep = 0">上一步</el-button>
      <el-button v-if="activeStep === 0" @click="nextStep">下一步</el-button>
      <el-button
        v-if="activeStep === 1"
        type="primary"
        :loading="saving"
        @click="saveExam"
      >
        保存
      </el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="resultVisible" title="考试成绩" width="820px">
    <el-table v-loading="resultLoading" :data="results" row-key="user_id">
      <el-table-column prop="username" label="用户名" min-width="140" />
      <el-table-column prop="class_name" label="班级" min-width="120">
        <template #default="{ row }">{{ row.class_name || "未分班" }}</template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="120" />
      <el-table-column prop="score" label="得分" width="100">
        <template #default="{ row }">{{ row.score ?? "-" }}</template>
      </el-table-column>
      <el-table-column prop="accepted_problems" label="通过题数" width="110" />
      <el-table-column prop="total_problems" label="总题数" width="90" />
      <el-table-column label="提交时间" min-width="180">
        <template #default="{ row }">{{ formatTime(row.submitted_at) }}</template>
      </el-table-column>
    </el-table>
    <div v-if="!resultLoading && results.length === 0" class="empty-state">
      暂无学生提交
    </div>
    <template #footer>
      <el-button :loading="exporting" @click="exportResults">导出成绩</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="previewVisible" title="考试预览" width="900px">
    <div v-loading="previewLoading">
      <template v-if="previewData">
        <div class="preview-head">
          <div>
            <h2>{{ previewData.title }}</h2>
            <p>{{ previewData.description || "无考试说明" }}</p>
          </div>
          <div class="preview-meta">
            <el-tag effect="plain">
              {{ statusLabel[previewData.status] || previewData.status }}
            </el-tag>
            <span>{{ previewData.duration_minutes }} 分钟</span>
            <span>{{ previewData.class_name || "全体学生" }}</span>
            <span>{{ previewData.problem_count }} 道题</span>
          </div>
        </div>
        <el-table :data="previewData.problems" row-key="problem_id">
          <el-table-column type="expand">
            <template #default="{ row }">
              <div class="preview-detail">
                <h4>{{ row.title }}</h4>
                <div class="preview-description">{{ row.description }}</div>
                <div v-if="row.test_cases?.length" class="case-list">
                  <div
                    v-for="(item, index) in row.test_cases"
                    :key="item.id"
                    class="case-item"
                  >
                    <div>示例 {{ index + 1 }}</div>
                    <div>输入：{{ item.input }}</div>
                    <div>预期输出：{{ item.expected_output }}</div>
                  </div>
                </div>
                <pre class="preview-code">{{ row.starter_code || "暂无起始代码" }}</pre>
              </div>
            </template>
          </el-table-column>
          <el-table-column type="index" label="#" width="72" />
          <el-table-column prop="title" label="题目" min-width="240" />
          <el-table-column prop="language" label="语言" width="120" />
          <el-table-column prop="question_type" label="题型" width="120" />
          <el-table-column label="分值" width="80">
            <template #default="{ row }">{{ row.score ?? "-" }}</template>
          </el-table-column>
          <el-table-column label="难度" width="110">
            <template #default="{ row }">
              {{ row.difficulty }}
            </template>
          </el-table-column>
          <el-table-column prop="tags" label="知识点" min-width="220" />
        </el-table>
      </template>
    </div>
  </el-dialog>
</template>

<style scoped>
.dialog-steps {
  margin-bottom: 20px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.auto-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}

.auto-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.field-label {
  color: #64748b;
  font-size: 13px;
  font-weight: 600;
}

.auto-options {
  display: grid;
  grid-template-columns: 150px 130px 130px auto;
  gap: 12px;
  align-items: end;
}

.stage-options {
  grid-template-columns: 180px;
}

.selected-block {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
  padding: 10px 12px;
  border-radius: 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
}

.selected-count {
  color: #176b5b;
  font-size: 13px;
  font-weight: 600;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  max-height: 140px;
  overflow-y: auto;
}

.preview-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 16px;
}

.preview-head h2 {
  margin: 0 0 6px;
  font-size: 20px;
}

.preview-head p {
  margin: 0;
  color: #64748b;
}

.preview-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #64748b;
  white-space: nowrap;
}

.preview-detail {
  padding: 4px 18px 18px 72px;
}

.preview-detail h4 {
  margin: 0 0 8px;
  font-size: 16px;
}

.preview-description {
  margin-bottom: 12px;
  color: #334155;
  white-space: pre-wrap;
}

.preview-code {
  margin: 12px 0 0;
  padding: 12px;
  overflow-x: auto;
  border-radius: 8px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  color: #1f2937;
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 13px;
  line-height: 1.55;
}
</style>
