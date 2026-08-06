<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import api from "../api";
import CodeEditor from "../components/CodeEditor.vue";
import { formatRichText } from "../format";

const route = useRoute();
const exam = ref(null);
const loading = ref(false);
const currentIndex = ref(0);
const code = ref("");
const result = ref(null);
const errorMessage = ref("");
const running = ref(false);
const submitting = ref(false);
const submittingExam = ref(false);
const timerText = ref("");
let saveTimer = null;
let timerInterval = null;
let autoSubmitted = false;

const EXAM_STARTERS = {
  python: "# 请根据题目要求完成代码\n",
  javascript: "// 请根据题目要求完成代码\n",
  java:
    "public class Main {\n" +
    "    public static void main(String[] args) {\n" +
    "        // 请根据题目要求完成代码\n" +
    "    }\n" +
    "}\n",
  cpp:
    "#include <iostream>\n" +
    "\n" +
    "int main() {\n" +
    "    // 请根据题目要求完成代码\n" +
    "    return 0;\n" +
    "}\n",
};

const currentProblem = computed(
  () => exam.value?.problems?.[currentIndex.value] || null,
);

async function loadExam() {
  loading.value = true;
  try {
    const { data } = await api.get(`/exams/${route.params.id}`);
    exam.value = data;
    result.value = null;
    errorMessage.value = "";
    if (data.attempt_status) {
      await loadProblemCode();
      startTimer();
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || error.message;
  } finally {
    loading.value = false;
  }
}

async function loadProblemCode() {
  const problem = currentProblem.value;
  if (!problem) return;
  code.value = EXAM_STARTERS[problem.language] || "";
  try {
    const { data: draft } = await api.get(`/drafts/${problem.problem_id}`);
    if (draft.code) {
      code.value = draft.code;
    }
  } catch {
    // no saved draft
  }
}

async function saveDraft() {
  const problem = currentProblem.value;
  if (!problem || exam.value?.attempt_status !== "in_progress") return;
  try {
    await api.put(`/drafts/${problem.problem_id}`, {
      code: code.value,
      language: problem.language,
    });
  } catch {
    // draft failure should not block exam submission
  }
}

async function selectProblem(index) {
  await saveDraft();
  currentIndex.value = index;
  await loadProblemCode();
}

async function startExam() {
  try {
    await api.post(`/exams/${route.params.id}/start`);
    await loadExam();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "开始考试失败");
  }
}

async function runCode() {
  const problem = currentProblem.value;
  if (!problem) return;
  running.value = true;
  result.value = null;
  errorMessage.value = "";
  try {
    const { data } = await api.post("/execute", {
      problem_id: problem.problem_id,
      code: code.value,
      language: problem.language,
    });
    result.value = data;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || error.message;
  } finally {
    running.value = false;
  }
}

async function submitProblem() {
  const problem = currentProblem.value;
  if (!problem || exam.value?.attempt_status !== "in_progress") return;
  submitting.value = true;
  result.value = null;
  errorMessage.value = "";
  try {
    const { data } = await api.post("/submissions", {
      problem_id: problem.problem_id,
      code: code.value,
      language: problem.language,
      exam_id: exam.value.id,
    });
    result.value = data;
    if (exam.value) {
      exam.value.results[String(problem.problem_id)] =
        data.status === "accepted" ? "accepted" : "submitted";
    }
    ElMessage.success(`提交结果：${data.status}`);
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || error.message;
  } finally {
    submitting.value = false;
  }
}

async function submitExam(force = false) {
  if (!force) {
    try {
      await ElMessageBox.confirm("提交后不能再修改答案，确定交卷吗？", "交卷", {
        type: "warning",
        confirmButtonText: "确认",
        cancelButtonText: "取消",
      });
    } catch {
      return;
    }
  }
  submittingExam.value = true;
  try {
    await saveDraft();
    const { data } = await api.post(`/exams/${exam.value.id}/submit`);
    ElMessage.success(`交卷成功：${data.score} 分`);
    await loadExam();
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "交卷失败");
  } finally {
    submittingExam.value = false;
  }
}

function formatSeconds(total) {
  const minutes = Math.floor(total / 60);
  const seconds = total % 60;
  return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function parseBackendDate(value) {
  if (!value) return null;
  const text = String(value);
  const hasTimezone = /[zZ]|[+-]\d{2}:\d{2}$/.test(text);
  return new Date(hasTimezone ? text : `${text}Z`);
}

function startTimer() {
  clearInterval(timerInterval);
  const update = () => {
    if (exam.value?.attempt_status !== "in_progress") {
      timerText.value = "";
      clearInterval(timerInterval);
      return;
    }
    const startedAt = parseBackendDate(exam.value.started_at)?.getTime() || Date.now();
    const deadline = startedAt + exam.value.duration_minutes * 60 * 1000;
    const remain = Math.max(0, Math.floor((deadline - Date.now()) / 1000));
    if (remain > 0) {
      timerText.value = formatSeconds(remain);
      return;
    }
    timerText.value = "时间到";
    clearInterval(timerInterval);
    if (!autoSubmitted) {
      autoSubmitted = true;
      submitExam(true);
    }
  };
  update();
  timerInterval = setInterval(update, 1000);
}

watch(code, () => {
  if (exam.value?.attempt_status !== "in_progress") return;
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveDraft, 800);
});

onMounted(loadExam);
onBeforeUnmount(() => {
  clearTimeout(saveTimer);
  clearInterval(timerInterval);
});
</script>

<template>
  <section v-if="exam" class="page">
    <div class="exam-head">
      <div>
        <h1>{{ exam.title }}</h1>
        <p>{{ exam.description || "无考试说明" }}</p>
      </div>
      <div v-if="exam.attempt_status === 'in_progress'" class="exam-timer">
        <span>剩余时间</span>
        <strong>{{ timerText }}</strong>
        <el-button type="danger" :loading="submittingExam" @click="submitExam()">
          交卷
        </el-button>
      </div>
    </div>

    <template v-if="!exam.attempt_status && exam.status === 'published'">
      <div class="panel empty-state">
        <p>考试时长：{{ exam.duration_minutes }} 分钟</p>
        <p>题目数量：{{ exam.problems.length }}</p>
        <el-button type="primary" @click="startExam">开始考试</el-button>
      </div>
    </template>

    <template v-else-if="exam.attempt_status === 'submitted'">
      <div class="stats-grid">
        <div class="stat-card">
          <strong>{{ exam.score }}</strong>
          <span>得分</span>
        </div>
        <div class="stat-card">
          <strong>{{ exam.accepted_problems }}/{{ exam.total_problems }}</strong>
          <span>通过题数</span>
        </div>
      </div>
      <div class="panel">
        <el-table :data="exam.problems" row-key="problem_id">
          <el-table-column prop="title" label="题目" min-width="220" />
          <el-table-column prop="language" label="语言" width="120" />
          <el-table-column label="结果" width="140">
            <template #default="{ row }">
              <el-tag
                :type="exam.results[String(row.problem_id)] === 'accepted' ? 'success' : 'info'"
                effect="plain"
              >
                {{ exam.results[String(row.problem_id)] === "accepted" ? "通过" : "未通过" }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </template>

    <template v-else-if="exam.attempt_status === 'in_progress'">
      <div class="work-grid">
        <section class="work-panel">
          <h3>题目列表</h3>
          <div class="problem-list">
            <button
              v-for="(problem, index) in exam.problems"
              :key="problem.problem_id"
              type="button"
              class="problem-item"
              :class="{ active: index === currentIndex }"
              @click="selectProblem(index)"
            >
              <span>{{ index + 1 }}. {{ problem.title }}</span>
              <el-tag
                v-if="exam.results[String(problem.problem_id)] === 'accepted'"
                type="success"
                size="small"
                effect="plain"
              >
                已通过
              </el-tag>
              <el-tag
                v-else-if="exam.results[String(problem.problem_id)]"
                type="warning"
                size="small"
                effect="plain"
              >
                已提交
              </el-tag>
            </button>
          </div>

          <div v-if="currentProblem" class="problem-meta">
            <el-tag effect="plain">{{ currentProblem.language }}</el-tag>
            <el-tag v-if="currentProblem.tags" type="info" effect="plain">
              {{ currentProblem.tags }}
            </el-tag>
          </div>
          <h2>{{ currentProblem?.title }}</h2>
          <div class="description" v-html="formatRichText(currentProblem?.description)"></div>
        </section>

        <section class="work-panel">
          <div class="editor-toolbar">
            <span class="role-chip">{{ currentProblem?.language || "python" }}</span>
            <div>
              <el-button :loading="running" @click="runCode">运行</el-button>
              <el-button
                type="primary"
                :loading="submitting"
                @click="submitProblem"
              >
                提交本题
              </el-button>
            </div>
          </div>
          <div class="editor-shell">
            <CodeEditor
              v-model="code"
              :language="currentProblem?.language || 'python'"
            />
          </div>

          <div v-if="errorMessage" class="result-block">
            <h3>请求失败</h3>
            <div class="case-item failed">{{ errorMessage }}</div>
          </div>

          <div v-if="result" class="result-block">
            <h3>执行结果：{{ result.status }}</h3>
            <div class="case-list">
              <div
                v-for="item in result.results"
                :key="item.case_id"
                class="case-item"
                :class="item.passed ? 'passed' : 'failed'"
              >
                <div>用例 {{ item.case_id }}：{{ item.passed ? "通过" : "未通过" }}</div>
                <div>期望：{{ item.expected_output }}</div>
                <div>实际：{{ item.actual_output || "（无输出）" }}</div>
                <div v-if="item.error">{{ item.error }}</div>
              </div>
              <div v-if="result.error_message" class="case-item failed">
                {{ result.error_message }}
              </div>
            </div>
          </div>
        </section>
      </div>
    </template>
  </section>

  <div v-else v-loading="loading" class="panel empty-state">加载考试中...</div>
</template>

<style scoped>
.exam-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 16px;
}

.exam-head h1 {
  margin: 0 0 6px;
  font-size: 24px;
}

.exam-head p {
  margin: 0;
  color: #64748b;
}

.exam-timer {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 16px;
  background: #ffffff;
  border: 1px solid #dde3e8;
  border-radius: 8px;
}

.exam-timer strong {
  font-size: 22px;
  color: #176b5b;
  font-variant-numeric: tabular-nums;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(140px, 220px));
  gap: 14px;
  margin-bottom: 16px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 18px;
  background: #ffffff;
  border: 1px solid #dde3e8;
  border-radius: 8px;
}

.stat-card strong {
  font-size: 28px;
  color: #176b5b;
}

.stat-card span {
  color: #64748b;
  font-size: 13px;
}

.problem-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 18px;
}

.problem-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #dde3e8;
  border-radius: 8px;
  background: #ffffff;
  color: #1f2937;
  text-align: left;
  cursor: pointer;
}

.problem-item.active {
  border-color: #176b5b;
  background: #f0f7f5;
}

.editor-shell {
  height: 420px;
  border: 1px solid #dde3e8;
  border-radius: 8px;
  overflow: hidden;
}
</style>
