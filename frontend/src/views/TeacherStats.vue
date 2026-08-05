<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from "vue";
import * as echarts from "echarts";
import api from "../api";

const stats = ref(null);
const loading = ref(false);
const passChartRef = ref(null);
const statusChartRef = ref(null);
const studentChartRef = ref(null);
const dailyChartRef = ref(null);
const charts = [];

async function loadStats() {
  loading.value = true;
  try {
    const { data } = await api.get("/admin/statistics");
    stats.value = data;
    await nextTick();
    renderCharts();
  } finally {
    loading.value = false;
  }
}

function disposeCharts() {
  charts.forEach((chart) => chart.dispose());
  charts.length = 0;
}

function renderCharts() {
  if (!stats.value) return;
  disposeCharts();

  const passChart = echarts.init(passChartRef.value);
  passChart.setOption({
    series: [
      {
        type: "gauge",
        startAngle: 220,
        endAngle: -40,
        min: 0,
        max: 100,
        radius: "92%",
        center: ["50%", "58%"],
        progress: {
          show: true,
          width: 16,
          roundCap: true,
          itemStyle: {
            color: {
              type: "linear",
              x: 0,
              y: 0,
              x2: 1,
              y2: 0,
              colorStops: [
                { offset: 0, color: "#10b981" },
                { offset: 1, color: "#38bdf8" },
              ],
            },
          },
        },
        axisLine: {
          lineStyle: {
            width: 16,
            color: [[1, "#eef2f5"]],
          },
        },
        pointer: { show: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: { show: false },
        detail: {
          valueAnimation: true,
          offsetCenter: [0, "18%"],
          formatter: "{value}%",
          fontSize: 30,
          fontWeight: 700,
          color: "#0f172a",
        },
        title: {
          offsetCenter: [0, "72%"],
          color: "#64748b",
          fontSize: 13,
        },
        data: [{ value: stats.value.pass_rate, name: "总通过率" }],
      },
    ],
  });
  charts.push(passChart);

  const statusChart = echarts.init(statusChartRef.value);
  statusChart.setOption({
    tooltip: { trigger: "item" },
    legend: { bottom: 0 },
    series: [
      {
        type: "pie",
        radius: ["42%", "68%"],
        center: ["50%", "46%"],
        data: [
          { name: "通过", value: stats.value.accepted_count, itemStyle: { color: "#16a34a" } },
          { name: "错误", value: stats.value.wrong_count, itemStyle: { color: "#f59e0b" } },
          { name: "运行错误", value: stats.value.error_count, itemStyle: { color: "#dc2626" } },
        ],
      },
    ],
  });
  charts.push(statusChart);

  const studentChart = echarts.init(studentChartRef.value);
  studentChart.setOption({
    tooltip: { trigger: "axis" },
    legend: { bottom: 0 },
    grid: { left: 40, right: 16, top: 28, bottom: 52 },
    xAxis: {
      type: "category",
      data: stats.value.students.map((item) => item.username),
    },
    yAxis: { type: "value", minInterval: 1 },
    series: [
      {
        name: "提交数",
        type: "bar",
        data: stats.value.students.map((item) => item.submission_count),
        itemStyle: { color: "#176b5b" },
      },
      {
        name: "通过数",
        type: "bar",
        data: stats.value.students.map((item) => item.accepted_count),
        itemStyle: { color: "#38bdf8" },
      },
    ],
  });
  charts.push(studentChart);

  const dailyChart = echarts.init(dailyChartRef.value);
  dailyChart.setOption({
    tooltip: { trigger: "axis" },
    legend: { bottom: 0 },
    grid: { left: 40, right: 16, top: 28, bottom: 52 },
    xAxis: {
      type: "category",
      data: stats.value.daily.map((item) => item.date.slice(5)),
    },
    yAxis: { type: "value", minInterval: 1 },
    series: [
      {
        name: "提交数",
        type: "line",
        smooth: true,
        data: stats.value.daily.map((item) => item.submissions),
        itemStyle: { color: "#176b5b" },
      },
      {
        name: "通过数",
        type: "line",
        smooth: true,
        data: stats.value.daily.map((item) => item.accepted),
        itemStyle: { color: "#38bdf8" },
      },
    ],
  });
  charts.push(dailyChart);
}

function resizeCharts() {
  charts.forEach((chart) => chart.resize());
}

watch(stats, () => {
  nextTick(renderCharts);
});

onMounted(() => {
  loadStats();
  window.addEventListener("resize", resizeCharts);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", resizeCharts);
  disposeCharts();
});
</script>

<template>
  <section class="page">
    <div v-if="stats" class="stats-grid">
      <div class="stat-card stat-green">
        <span class="stat-label">学生总数</span>
        <strong>{{ stats.total_students }}</strong>
      </div>
      <div class="stat-card stat-blue">
        <span class="stat-label">提交总数</span>
        <strong>{{ stats.total_submissions }}</strong>
      </div>
      <div class="stat-card stat-amber">
        <span class="stat-label">通过</span>
        <strong>{{ stats.accepted_count }}</strong>
      </div>
      <div class="stat-card stat-indigo">
        <span class="stat-label">总通过率</span>
        <strong>{{ stats.pass_rate }}%</strong>
      </div>
    </div>

    <div class="chart-grid">
      <div class="chart-card">
        <h3 class="chart-title">总通过率</h3>
        <div ref="passChartRef" class="chart"></div>
      </div>
      <div class="chart-card">
        <h3 class="chart-title">提交状态分布</h3>
        <div ref="statusChartRef" class="chart"></div>
      </div>
      <div class="chart-card chart-wide">
        <h3 class="chart-title">学生提交情况</h3>
        <div ref="studentChartRef" class="chart"></div>
      </div>
      <div class="chart-card chart-wide">
        <h3 class="chart-title">最近 7 天提交趋势</h3>
        <div ref="dailyChartRef" class="chart"></div>
      </div>
    </div>

    <div class="page-head">
      <div>
        <h1>学生明细</h1>
        <p v-if="stats">{{ stats.students.length }} 个学生账号</p>
      </div>
      <el-button @click="loadStats">刷新</el-button>
    </div>

    <div class="panel">
      <el-table v-loading="loading" :data="stats?.students || []" row-key="user_id">
        <el-table-column prop="user_id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" min-width="140" />
        <el-table-column prop="email" label="邮箱" min-width="200" />
        <el-table-column prop="submission_count" label="提交数" width="100" />
        <el-table-column prop="accepted_count" label="通过数" width="100" />
        <el-table-column prop="pass_rate" label="通过率" width="110">
          <template #default="{ row }">{{ row.pass_rate }}%</template>
        </el-table-column>
      </el-table>
    </div>
  </section>
</template>

<style scoped>
.stat-card {
  position: relative;
  overflow: hidden;
  min-height: 96px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
  padding: 16px 18px;
  background: #ffffff;
  border: 1px solid #dde3e8;
  border-radius: 8px;
}

.stat-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: var(--accent, #176b5b);
}

.stat-green {
  --accent: #10b981;
}

.stat-blue {
  --accent: #38bdf8;
}

.stat-amber {
  --accent: #f59e0b;
}

.stat-indigo {
  --accent: #6366f1;
}

.stat-label {
  color: #64748b;
  font-size: 13px;
  font-weight: 600;
}

.stat-card strong {
  font-size: 30px;
  line-height: 1;
  color: #0f172a;
}

.chart-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.chart-card {
  background: #ffffff;
  border: 1px solid #dde3e8;
  border-radius: 8px;
  padding: 10px;
}

.chart-title {
  margin: 2px 4px 8px;
  font-size: 15px;
  color: #1f2937;
}

.chart-wide {
  grid-column: span 2;
}

.chart {
  width: 100%;
  height: 300px;
}
</style>
