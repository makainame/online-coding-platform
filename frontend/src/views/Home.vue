<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import api from "../api";

const router = useRouter();
const problems = ref([]);
const loading = ref(false);
const keyword = ref("");
const difficulty = ref("");
const expandedLanguages = ref(["python", "javascript", "java", "cpp"]);

const languageLabel = {
  python: "Python",
  java: "Java",
  javascript: "JavaScript",
  cpp: "C++",
};

const difficultyClass = {
  easy: "",
  medium: "warning",
  hard: "danger",
};

const difficultyLabel = {
  easy: "简单",
  medium: "中等",
  hard: "困难",
};

const difficultyRank = {
  easy: 1,
  medium: 2,
  hard: 3,
};

const hasToken = computed(() => Boolean(localStorage.getItem("token")));

function teachingRank(tags) {
  const dayTag = tags.split(",").find((tag) => /^(进阶)?Day\d+$/.test(tag));
  if (!dayTag) return 100;
  const advanced = dayTag.startsWith("进阶") ? 10 : 0;
  return advanced + Number(dayTag.replace("进阶", "").replace("Day", ""));
}

const filtered = computed(() => {
  const q = keyword.value.trim();
  const list = problems.value.filter(
    (item) =>
      (!q || item.title.includes(q) || item.tags.includes(q)) &&
      (!difficulty.value || item.difficulty === difficulty.value)
  );
  return [...list].sort(
    (a, b) =>
      teachingRank(a.tags) - teachingRank(b.tags) ||
      a.id - b.id
  );
});

const languages = computed(() => {
  const groups = new Map();
  for (const item of filtered.value) {
    const language = item.language || "python";
    if (!groups.has(language)) groups.set(language, []);
    groups.get(language).push(item);
  }
  return [...groups.entries()]
    .map(([language, items]) => ({
      language,
      label: languageLabel[language] || language,
      items,
    }))
    .sort((a, b) => {
      if (a.language === "python") return -1;
      if (b.language === "python") return 1;
      return a.label.localeCompare(b.label, "zh-CN");
    });
});

async function loadProblems() {
  if (!hasToken.value) return;
  loading.value = true;
  try {
    const { data } = await api.get("/problems");
    problems.value = data;
  } finally {
    loading.value = false;
  }
}

function openProblem(id) {
  router.push(`/problem/${id}`);
}

function clearFilters() {
  keyword.value = "";
  difficulty.value = "";
}

onMounted(loadProblems);
</script>

<template>
  <section class="page">
    <div class="page-head">
      <div>
        <h1>练习题库</h1>
        <p>{{ loading ? "题库加载中..." : `${problems.length} 道题目` }}</p>
      </div>
      <div class="filter-bar">
        <el-input
          v-model="keyword"
          placeholder="搜索题目或标签"
          clearable
          style="max-width: 300px"
        />
        <el-select
          v-model="difficulty"
          placeholder="难度"
          clearable
          style="width: 140px"
        >
          <el-option label="简单" value="easy" />
          <el-option label="中等" value="medium" />
          <el-option label="困难" value="hard" />
        </el-select>
      </div>
    </div>

    <div class="panel">
      <div v-if="loading" class="question-skeleton">
        <div v-for="group in 3" :key="group" class="skeleton-group">
          <div class="skeleton-title"></div>
          <div class="skeleton-table">
            <div v-for="row in 5" :key="row" class="skeleton-row">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>

      <template v-else>
        <el-collapse v-model="expandedLanguages" class="language-collapse">
          <el-collapse-item
            v-for="group in languages"
            :key="group.language"
            :name="group.language"
          >
            <template #title>
              <div class="language-title">
                <span class="language-badge">{{ group.label }}</span>
                <span class="language-count">{{ group.items.length }} 道</span>
              </div>
            </template>
            <el-table
              :data="group.items"
              row-key="id"
              @row-click="(row) => openProblem(row.id)"
            >
              <el-table-column type="index" label="#" width="72" />
              <el-table-column prop="title" label="题目" min-width="240" />
              <el-table-column prop="language" label="语言" width="100" />
              <el-table-column prop="tags" label="标签" min-width="180" />
              <el-table-column label="难度" width="110">
                <template #default="{ row }">
                  <el-tag :type="difficultyClass[row.difficulty]" effect="plain">
                    {{ difficultyLabel[row.difficulty] || row.difficulty }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="" width="90">
                <template #default>
                  <span class="open-link">打开</span>
                </template>
              </el-table-column>
            </el-table>
          </el-collapse-item>
        </el-collapse>

        <div v-if="filtered.length === 0" class="empty-state">
          <svg
            class="empty-icon"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <circle cx="11" cy="11" r="7" />
            <line x1="16.5" y1="16.5" x2="21" y2="21" />
          </svg>
          <p>{{ hasToken ? "暂无匹配题目" : "登录后查看题库" }}</p>
          <p v-if="hasToken" class="empty-hint">换个关键词或难度试试</p>
          <el-button
            v-if="hasToken && (keyword || difficulty)"
            @click="clearFilters"
          >
            清除筛选
          </el-button>
        </div>
      </template>
    </div>
  </section>
</template>

<style scoped>
.filter-bar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.open-link {
  color: #176b5b;
  font-weight: 600;
}

.language-collapse {
  border: 0;
}

.language-collapse :deep(.el-collapse-item__header) {
  height: 48px;
  padding: 0 16px;
  background: #f8fafc;
  border-bottom: 1px solid #eef1f4;
}

.language-collapse :deep(.el-collapse-item__wrap) {
  border-bottom: 0;
}

.language-title {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.language-badge {
  padding: 0;
  background: transparent;
  color: #334155;
  font-size: 14px;
  font-weight: 700;
}

.language-count {
  color: #64748b;
  font-size: 12px;
}

.empty-icon {
  width: 42px;
  height: 42px;
  margin-bottom: 8px;
  color: #94a3b8;
}

.empty-hint {
  margin: 6px 0 0;
  color: #94a3b8;
  font-size: 13px;
}

.question-skeleton {
  display: flex;
  flex-direction: column;
  gap: 18px;
  padding: 18px;
}

.skeleton-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton-title {
  width: 180px;
  height: 18px;
  border-radius: 6px;
  background: linear-gradient(90deg, #edf1f4 25%, #e2e8ed 37%, #edf1f4 63%);
  background-size: 400% 100%;
  animation: skeleton-shimmer 1.4s ease infinite;
}

.skeleton-table {
  border: 1px solid #eef1f4;
  border-radius: 8px;
  overflow: hidden;
}

.skeleton-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 16px;
  padding: 16px 18px;
  border-bottom: 1px solid #eef1f4;
}

.skeleton-row:last-child {
  border-bottom: 0;
}

.skeleton-row span {
  height: 12px;
  border-radius: 6px;
  background: linear-gradient(90deg, #edf1f4 25%, #e2e8ed 37%, #edf1f4 63%);
  background-size: 400% 100%;
  animation: skeleton-shimmer 1.4s ease infinite;
}

@keyframes skeleton-shimmer {
  0% {
    background-position: 100% 0;
  }
  100% {
    background-position: 0 0;
  }
}

:deep(.el-table__row) {
  cursor: pointer;
}
</style>
