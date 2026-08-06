<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import api from "../api";

const router = useRouter();
const exams = ref([]);
const loading = ref(false);

const statusLabel = {
  draft: "草稿",
  published: "已发布",
  closed: "已关闭",
};

async function loadExams() {
  loading.value = true;
  try {
    const { data } = await api.get("/exams");
    exams.value = data;
  } finally {
    loading.value = false;
  }
}

function actionLabel(row) {
  if (row.attempt_status === "submitted") return "查看结果";
  if (row.attempt_status === "in_progress") return "继续考试";
  return "开始考试";
}

function openExam(row) {
  router.push(`/exam/${row.id}`);
}

onMounted(loadExams);
</script>

<template>
  <section class="page">
    <div class="page-head">
      <div>
        <h1>我的考试</h1>
        <p>{{ exams.length }} 场可参加或已参加的考试</p>
      </div>
      <el-button @click="loadExams">刷新</el-button>
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
            {{ statusLabel[row.status] || row.status }}
          </template>
        </el-table-column>
        <el-table-column prop="duration_minutes" label="时长(分钟)" width="120" />
        <el-table-column label="我的状态" width="130">
          <template #default="{ row }">
            <span v-if="row.attempt_status === 'submitted'">已提交</span>
            <span v-else-if="row.attempt_status === 'in_progress'">考试中</span>
            <span v-else>未开始</span>
          </template>
        </el-table-column>
        <el-table-column label="得分" width="100">
          <template #default="{ row }">
            <template v-if="row.attempt_status === 'submitted'">
              {{ row.score }}（{{ row.accepted_problems }}/{{ row.total_problems }}）
            </template>
            <template v-else>-</template>
          </template>
        </el-table-column>
        <el-table-column label="" width="120">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'published' || row.attempt_status"
              type="primary"
              link
              @click="openExam(row)"
            >
              {{ actionLabel(row) }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="!loading && exams.length === 0" class="empty-state">
        暂无考试
      </div>
    </div>
  </section>
</template>
