<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import api from "../api";

const defaultJson = `[
  {
    "title": "求平方",
    "description": "输入一个整数 n，输出 n 的平方。",
    "language": "python",
    "difficulty": "easy",
    "tags": "入门,运算",
    "starter_code": "n = int(input())\\nprint(n * n)\\n",
    "test_cases": [
      { "input": "3", "expected_output": "9", "is_sample": true },
      { "input": "5", "expected_output": "25", "is_sample": true }
    ]
  }
]`;
const jsonText = ref(defaultJson);
const importing = ref(false);
const result = ref(null);

async function importProblems() {
  importing.value = true;
  result.value = null;
  let payload;
  try {
    payload = JSON.parse(jsonText.value);
  } catch (error) {
    ElMessage.error(`JSON 格式错误：${error.message}`);
    importing.value = false;
    return;
  }

  if (!Array.isArray(payload) || payload.length === 0) {
    ElMessage.error("题库内容必须是非空数组");
    importing.value = false;
    return;
  }

  try {
    const { data } = await api.post("/problems/import", payload);
    result.value = data;
    ElMessage.success(`导入完成：新增 ${data.created}，更新 ${data.updated}`);
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "导入失败");
  } finally {
    importing.value = false;
  }
}

function resetTemplate() {
  jsonText.value = defaultJson;
  result.value = null;
}
</script>

<template>
  <section class="page">
    <div class="page-head">
      <div>
        <h1>题库管理</h1>
        <p>支持 JSON 批量导入题目，导入后可在练习题库中查看</p>
      </div>
      <el-button @click="resetTemplate">恢复模板</el-button>
    </div>

    <div class="panel">
      <div class="import-form">
        <el-input
          v-model="jsonText"
          type="textarea"
          :rows="18"
          class="json-input"
        />
        <div class="import-actions">
          <el-button type="primary" :loading="importing" @click="importProblems">
            导入题库
          </el-button>
        </div>

        <div v-if="result" class="result-block">
          <h3>导入结果</h3>
          <div class="case-item passed">
            共 {{ result.total }} 条，新增 {{ result.created }}，更新
            {{ result.updated }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.import-form {
  padding: 20px;
}

.json-input {
  font-family: "Cascadia Code", Consolas, monospace;
}

.import-actions {
  margin-top: 14px;
}
</style>
