<script setup>
import { onMounted, ref } from "vue";
import api from "../api";

const submissions = ref([]);
const loading = ref(false);
const detail = ref(null);
const detailLoading = ref(false);
const detailVisible = ref(false);
const feedback = ref(null);
const stats = ref(null);
const daily = ref(null);
const dailyLoading = ref(false);
const dateFilter = ref("");
const isTeacher = ref(false);
const difficultyLabel = {
  easy: "简单",
  medium: "中等",
  hard: "困难",
};

const statusType = {
  accepted: "success",
  wrong_answer: "warning",
  error: "danger",
  pending: "info",
  running: "info",
};

function localDateString(value = new Date()) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

async function loadSubmissions() {
  loading.value = true;
  try {
    const { data } = await api.get("/submissions", {
      params: dateFilter.value ? { date: dateFilter.value } : {},
    });
    submissions.value = data;
  } finally {
    loading.value = false;
  }
}

async function loadDaily() {
  if (!isTeacher.value || !dateFilter.value) return;
  dailyLoading.value = true;
  try {
    const { data } = await api.get("/admin/submissions/daily", {
      params: { date: dateFilter.value },
    });
    daily.value = data;
  } catch {
    daily.value = null;
  } finally {
    dailyLoading.value = false;
  }
}

function onDateChange() {
  loadSubmissions();
  loadDaily();
}

async function loadUserRole() {
  try {
    const { data } = await api.get("/users/me");
    isTeacher.value = data.role === "teacher";
  } catch {
    isTeacher.value = false;
  }
}

async function loadStats() {
  try {
    const { data } = await api.get("/statistics/me");
    stats.value = data;
  } catch {
    stats.value = null;
  }
}

async function showDetail(row) {
  detailVisible.value = true;
  detailLoading.value = true;
  detail.value = null;
  feedback.value = null;
  try {
    const { data } = await api.get(`/submissions/${row.id}`);
    detail.value = data;
    try {
      const { data: fb } = await api.get(`/feedback/${row.id}`);
      feedback.value = fb;
    } catch {
      feedback.value = null;
    }
  } finally {
    detailLoading.value = false;
  }
}

function formatTime(value) {
  return value ? new Date(value).toLocaleString() : "-";
}

onMounted(async () => {
  dateFilter.value = localDateString();
  await loadUserRole();
  loadSubmissions();
  loadStats();
  loadDaily();
});
</script>

<template>
  <section class="page">
    <div v-if="stats" class="stats-grid">
      <div class="stat-card">
        <strong>{{ stats.total_submissions }}</strong>
        <span>总提交</span>
      </div>
      <div class="stat-card">
        <strong>{{ stats.accepted_count }}</strong>
        <span>通过</span>
      </div>
      <div class="stat-card">
        <strong>{{ stats.pass_rate }}%</strong>
        <span>通过率</span>
      </div>
      <div class="stat-card">
        <strong>{{ stats.today_count }}</strong>
        <span>今日提交</span>
      </div>
      <div class="stat-card daily-card">
        <strong>最近 7 天</strong>
        <div class="daily-strip">
          <div v-for="item in stats.daily" :key="item.date" class="daily-item">
            <span>{{ item.date.slice(5) }}</span>
            <span class="daily-count">{{ item.submissions }}</span>
            <span class="daily-pass">{{ item.accepted }} 通过</span>
          </div>
        </div>
      </div>
      <div class="stat-card">
        <strong>难度分布</strong>
        <div class="difficulty-list">
          <div v-for="item in stats.by_difficulty" :key="item.difficulty">
            <span>{{ difficultyLabel[item.difficulty] || item.difficulty }}</span>
            <span>{{ item.submissions }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isTeacher" class="panel daily-panel">
      <div class="daily-head">
        <h3>按日提交统计</h3>
        <el-date-picker
          v-model="dateFilter"
          type="date"
          value-format="YYYY-MM-DD"
          placeholder="选择日期"
          @change="onDateChange"
        />
      </div>
      <div v-loading="dailyLoading">
        <div v-if="daily" class="daily-cards">
          <div class="stat-card">
            <strong>{{ daily.submitted_students }}</strong>
            <span>已提交学生</span>
          </div>
          <div class="stat-card">
            <strong>{{ daily.not_submitted_students }}</strong>
            <span>未提交学生</span>
          </div>
        </div>
        <el-table v-if="daily" :data="daily.students" row-key="user_id">
          <el-table-column type="index" label="#" width="80" :index="(index) => index + 1" />
          <el-table-column prop="username" label="学生" min-width="140" />
          <el-table-column prop="class_name" label="班级" min-width="140">
            <template #default="{ row }">{{ row.class_name || "未分班" }}</template>
          </el-table-column>
          <el-table-column label="状态" width="110">
            <template #default="{ row }">
              <el-tag
                :type="row.submission_count > 0 ? 'success' : 'info'"
                effect="plain"
              >
                {{ row.submission_count > 0 ? "已提交" : "未提交" }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="submission_count" label="当日提交次数" width="130" />
          <el-table-column prop="accepted_count" label="通过次数" width="110" />
          <el-table-column label="最新结果" width="120">
            <template #default="{ row }">
              {{
                row.latest_status === "accepted"
                  ? "通过"
                  : row.latest_status === "wrong_answer"
                    ? "未通过"
                    : row.latest_status === "error"
                      ? "运行错误"
                      : "-"
              }}
            </template>
          </el-table-column>
          <el-table-column label="最新提交时间" min-width="180">
            <template #default="{ row }">{{ formatTime(row.latest_time) }}</template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <div class="page-head">
      <div>
        <h1>提交记录</h1>
        <p>{{ submissions.length }} 条记录</p>
      </div>
      <el-button @click="loadSubmissions">刷新</el-button>
    </div>

    <div class="panel">
      <el-table v-loading="loading" :data="submissions" row-key="id">
        <el-table-column type="index" label="#" width="80" :index="(index) => index + 1" />
        <el-table-column prop="username" label="学生" min-width="120" />
        <el-table-column
          prop="problem_title"
          label="题目"
          min-width="220"
          show-overflow-tooltip
        />
        <el-table-column prop="language" label="语言" width="110" />
        <el-table-column label="状态" width="130">
          <template #default="{ row }">
            <el-tag :type="statusType[row.status]" effect="plain">
              {{ row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="execution_time" label="耗时(s)" width="120" />
        <el-table-column label="提交时间" min-width="190">
          <template #default="{ row }">{{ formatTime(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="" width="90">
          <template #default="{ row }">
            <el-button link type="primary" @click="showDetail(row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="!loading && submissions.length === 0" class="empty-state">
        暂无提交记录
      </div>
    </div>
  </section>

  <el-dialog v-model="detailVisible" title="提交详情" width="760px">
    <div v-loading="detailLoading">
      <template v-if="detail">
        <div class="detail-grid">
          <div><strong>状态：</strong>{{ detail.status }}</div>
          <div><strong>耗时：</strong>{{ detail.execution_time ?? "-" }}s</div>
        </div>
        <div class="detail-section">
          <h3>代码</h3>
          <pre class="code-block">{{ detail.code }}</pre>
        </div>
        <div v-if="detail.actual_output" class="detail-section">
          <h3>实际输出</h3>
          <pre class="code-block">{{ detail.actual_output }}</pre>
        </div>
        <div v-if="detail.error_message" class="detail-section">
          <h3>错误信息</h3>
          <pre class="code-block error-text">{{ detail.error_message }}</pre>
        </div>
        <div v-if="feedback" class="detail-section">
          <h3>AI 反馈 · {{ feedback.score }} 分</h3>
          <pre class="code-block">{{ feedback.feedback_text }}</pre>
        </div>
      </template>
    </div>
  </el-dialog>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(120px, 1fr));
  gap: 12px;
}

.daily-panel {
  margin-bottom: 14px;
}

.daily-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.daily-head h3 {
  margin: 0;
  font-size: 16px;
  color: #1f2937;
}

.daily-cards {
  display: grid;
  grid-template-columns: repeat(2, minmax(120px, 1fr));
  gap: 12px;
  margin-bottom: 12px;
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
  font-size: 22px;
  color: #176b5b;
}

.stat-card span {
  color: #64748b;
  font-size: 13px;
}

.daily-card {
  grid-column: span 2;
}

.daily-strip {
  display: flex;
  gap: 8px;
  overflow-x: auto;
}

.daily-item {
  min-width: 56px;
  padding: 8px;
  background: #f4f7f6;
  border-radius: 6px;
  text-align: center;
}

.daily-count {
  display: block;
  font-size: 16px;
  font-weight: 700;
  color: #1f2937;
}

.daily-pass {
  display: block;
  font-size: 11px;
  color: #176b5b;
}

.difficulty-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.difficulty-list div {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.detail-grid {
  display: flex;
  gap: 24px;
  margin-bottom: 14px;
}

.detail-section {
  margin-top: 14px;
}

.detail-section h3 {
  margin: 0 0 8px;
  font-size: 14px;
}

.code-block {
  max-height: 260px;
  overflow: auto;
  margin: 0;
  padding: 12px;
  background: #0f172a;
  color: #e2e8f0;
  border-radius: 6px;
  white-space: pre-wrap;
  font-family: "Cascadia Code", Consolas, monospace;
  font-size: 12px;
  line-height: 1.6;
}

.error-text {
  color: #fecaca;
}
</style>
