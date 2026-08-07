<script setup>
import { onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { ArrowLeft } from "@element-plus/icons-vue";
import api from "../api";
import CodeEditor from "../components/CodeEditor.vue";
import { formatRichText } from "../format";

const route = useRoute();
const router = useRouter();
const problem = ref(null);
const DEFAULT_CODE = `def solve():
    data = input().strip()
    # 请根据题目要求处理 data 并输出结果
    print(data)

solve()
`;
const code = ref(DEFAULT_CODE);
const loading = ref(false);
const running = ref(false);
const submitting = ref(false);
const result = ref(null);
const feedback = ref(null);
const feedbackLoading = ref(false);
const errorMessage = ref("");
const customInput = ref("");
const showCustomInput = ref(false);
const draftStatus = ref("");
let saveTimer = null;
const difficultyLabel = {
  easy: "简单",
  medium: "中等",
  hard: "困难",
};

async function loadProblem() {
  loading.value = true;
  try {
    const { data } = await api.get(`/problems/${route.params.id}`);
    problem.value = data;
    if (data.starter_code) {
      code.value = data.starter_code;
    }
    try {
      const { data: draft } = await api.get(`/drafts/${route.params.id}`);
      if (draft.code) {
        code.value = draft.code;
        draftStatus.value = "已加载草稿";
      }
    } catch {
      draftStatus.value = "";
    }
  } finally {
    loading.value = false;
  }
}

watch(code, (value) => {
  if (!problem.value) return;
  draftStatus.value = "保存中...";
  clearTimeout(saveTimer);
  saveTimer = setTimeout(async () => {
    try {
      await api.put(`/drafts/${problem.value.id}`, {
        code: value,
        language: problem.value.language || "python",
      });
      draftStatus.value = "已自动保存";
    } catch {
      draftStatus.value = "保存失败";
    }
  }, 800);
});

async function runCode() {
  running.value = true;
  errorMessage.value = "";
  result.value = null;
  feedback.value = null;
  try {
    const payload = {
      problem_id: Number(route.params.id),
      code: code.value,
      language: problem.value.language || "python",
    };
    if (customInput.value.trim() !== "") {
      payload.custom_input = customInput.value;
    }
    const { data } = await api.post("/execute", payload);
    result.value = data;
    await loadRunFeedback(payload);
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || error.message;
  } finally {
    running.value = false;
  }
}

async function loadRunFeedback(payload) {
  feedbackLoading.value = true;
  try {
    const { data } = await api.post("/execute/feedback", payload);
    feedback.value = data;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || error.message;
  } finally {
    feedbackLoading.value = false;
  }
}

async function submitCode() {
  submitting.value = true;
  errorMessage.value = "";
  result.value = null;
  feedback.value = null;
  try {
    const { data } = await api.post("/submissions", {
      problem_id: Number(route.params.id),
      code: code.value,
      language: problem.value.language || "python",
    });
    result.value = data;
    await loadFeedback(data.id);
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || error.message;
  } finally {
    submitting.value = false;
  }
}

async function loadFeedback(submissionId) {
  feedbackLoading.value = true;
  try {
    const { data } = await api.post(`/feedback/${submissionId}`);
    feedback.value = data;
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || error.message;
  } finally {
    feedbackLoading.value = false;
  }
}

function goBack() {
  router.push("/");
}

onMounted(loadProblem);
</script>

<template>
  <div class="problem-nav">
    <el-tooltip content="返回题库" placement="top">
      <el-button
        :icon="ArrowLeft"
        circle
        plain
        type="primary"
        aria-label="返回题库"
        @click="goBack"
      />
    </el-tooltip>
  </div>

  <div v-if="problem" class="work-grid">
    <section class="work-panel">
      <div class="problem-meta">
        <el-tag effect="plain">
          {{ difficultyLabel[problem.difficulty] || problem.difficulty }}
        </el-tag>
        <el-tag v-if="problem.tags" type="info" effect="plain">
          {{ problem.tags }}
        </el-tag>
      </div>
      <h2>{{ problem.title }}</h2>
      <div class="description" v-html="formatRichText(problem.description)"></div>

      <div v-if="problem.test_cases?.length" class="result-block">
        <h3>示例用例</h3>
        <div class="case-list">
          <div
            v-for="(item, index) in problem.test_cases"
            :key="item.id"
            class="case-item"
          >
            <div>输入：{{ item.input }}</div>
            <div>预期输出：{{ item.expected_output }}</div>
          </div>
        </div>
      </div>

      <div class="result-block">
        <div class="editor-toolbar">
          <span class="role-chip">自定义输入</span>
          <el-button link type="primary" @click="showCustomInput = !showCustomInput">
            {{ showCustomInput ? "收起" : "展开" }}
          </el-button>
        </div>
        <el-input
          v-if="showCustomInput"
          v-model="customInput"
          type="textarea"
          :rows="4"
          placeholder="输入测试数据"
        />
      </div>
    </section>

    <section class="work-panel">
      <div class="editor-toolbar">
        <span class="role-chip">{{ problem.language || "python" }}</span>
        <span v-if="draftStatus" class="draft-status">{{ draftStatus }}</span>
        <div>
          <el-button :loading="running" @click="runCode">运行</el-button>
          <el-button type="primary" :loading="submitting" @click="submitCode">
            提交
          </el-button>
        </div>
      </div>
      <div class="editor-shell">
        <CodeEditor v-model="code" :language="problem.language || 'python'" />
      </div>

      <div v-if="errorMessage" class="result-block">
        <h3>请求失败</h3>
        <div class="case-item failed">{{ errorMessage }}</div>
      </div>

      <div v-if="result" class="result-block">
        <h3>
          执行结果：{{ result.status }} · {{ result.execution_time }}s
        </h3>
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

      <div class="feedback-box">
        <h3>AI 反馈<span v-if="feedback"> · {{ feedback.score }} 分</span></h3>
        <div v-if="feedbackLoading" class="feedback-text">正在生成反馈...</div>
        <div v-else-if="feedback" class="feedback-text">{{ feedback.feedback_text }}</div>
        <div v-else class="feedback-empty">运行或提交后自动生成</div>
      </div>
    </section>
  </div>

  <div v-else v-loading="loading" class="panel empty-state">加载题目中...</div>
</template>

<style scoped>
.problem-nav {
  margin-bottom: 12px;
}

.draft-status {
  color: #64748b;
  font-size: 12px;
}

.feedback-empty {
  color: #64748b;
}
</style>
