<script setup>
import { onMounted, reactive, ref, watch } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import api from "../api";

const form = reactive({
  provider: "deepseek",
  base_url: "",
  model: "",
  api_key: "",
});
const AI_PRESETS = {
  deepseek: {
    base_url: "https://api.deepseek.com/v1",
    model: "deepseek-v4-flash",
  },
  qwen: {
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    model: "qwen3.7-plus",
  },
};
const savedInfo = ref({
  has_key: false,
  masked_key: "",
});
const saving = ref(false);
const deleting = ref(false);
const testing = ref(false);
const testResult = ref(null);

watch(
  () => form.provider,
  (provider) => {
    const preset = AI_PRESETS[provider] || AI_PRESETS.deepseek;
    form.base_url = preset.base_url;
    form.model = preset.model;
  }
);

async function loadSettings() {
  try {
    const { data } = await api.get("/ai/settings");
    form.provider = data.provider;
    form.base_url = data.base_url;
    form.model = data.model;
    savedInfo.value = {
      has_key: data.has_key,
      masked_key: data.masked_key,
    };
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "加载 AI 配置失败");
  }
}

async function saveSettings() {
  saving.value = true;
  try {
    const { data } = await api.put("/ai/settings", {
      provider: form.provider,
      base_url: form.base_url,
      model: form.model,
      api_key: form.api_key || undefined,
    });
    savedInfo.value = {
      has_key: data.has_key,
      masked_key: data.masked_key,
    };
    form.api_key = "";
    testResult.value = null;
    ElMessage.success("AI 配置已保存");
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "保存失败");
  } finally {
    saving.value = false;
  }
}

async function testSettings() {
  testing.value = true;
  testResult.value = null;
  try {
    const { data } = await api.post("/ai/settings/test", {
      provider: form.provider,
      base_url: form.base_url,
      model: form.model,
      api_key: form.api_key || undefined,
    });
    testResult.value = data;
  } catch (error) {
    testResult.value = {
      ok: false,
      message: error.response?.data?.detail || error.message,
    };
  } finally {
    testing.value = false;
  }
}

async function deleteKey() {
  try {
    await ElMessageBox.confirm("确定删除已保存的 API Key？", "删除 Key", {
      type: "warning",
    });
  } catch {
    return;
  }

  deleting.value = true;
  try {
    await api.delete("/ai/settings");
    savedInfo.value = {
      has_key: false,
      masked_key: "",
    };
    form.api_key = "";
    testResult.value = null;
    ElMessage.success("API Key 已删除");
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || "删除失败");
  } finally {
    deleting.value = false;
  }
}

onMounted(loadSettings);
</script>

<template>
  <section class="page">
    <div class="page-head">
      <div>
        <h1>AI 配置</h1>
        <p v-if="savedInfo.has_key">已配置：{{ savedInfo.masked_key }}</p>
        <p v-else>尚未配置自己的 API Key</p>
      </div>
    </div>

    <div class="panel">
      <div class="ai-form">
        <el-form label-position="top">
          <el-form-item label="AI 服务商">
            <el-radio-group v-model="form.provider">
              <el-radio value="deepseek">DeepSeek</el-radio>
              <el-radio value="qwen">通义千问</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="API 地址">
            <el-input v-model="form.base_url" />
          </el-form-item>
          <el-form-item label="模型">
            <el-input v-model="form.model" />
          </el-form-item>
          <el-form-item label="自己的 API Key">
            <el-input
              v-model="form.api_key"
              type="password"
              show-password
              placeholder="留空表示不修改已保存的 Key"
            />
          </el-form-item>
        </el-form>

        <div class="ai-actions">
          <el-button :loading="testing" @click="testSettings">测试连接</el-button>
          <el-button type="primary" :loading="saving" @click="saveSettings">
            保存配置
          </el-button>
          <el-button type="danger" :loading="deleting" @click="deleteKey">
            删除 Key
          </el-button>
        </div>

        <div v-if="testResult" class="result-block">
          <h3>{{ testResult.ok ? "连接成功" : "连接失败" }}</h3>
          <div class="case-item" :class="testResult.ok ? 'passed' : 'failed'">
            {{ testResult.message }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.ai-form {
  max-width: 560px;
  padding: 20px;
}

.ai-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 14px;
}
</style>
