<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from "vue";
import * as monaco from "monaco-editor";
import editorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";

globalThis.MonacoEnvironment = {
  getWorker() {
    return new editorWorker();
  },
};

const props = defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  language: {
    type: String,
    default: "python",
  },
});

const emit = defineEmits(["update:modelValue"]);
const el = ref(null);
let editor = null;

onMounted(() => {
  editor = monaco.editor.create(el.value, {
    value: props.modelValue,
    language: props.language,
    theme: "vs",
    automaticLayout: true,
    minimap: { enabled: false },
    fontSize: 14,
    lineNumbersMinChars: 3,
    scrollBeyondLastLine: false,
  });
  editor.onDidChangeModelContent(() => {
    emit("update:modelValue", editor.getValue());
  });
});

watch(
  () => props.modelValue,
  (value) => {
    if (editor && editor.getValue() !== value) {
      editor.setValue(value);
    }
  }
);

watch(
  () => props.language,
  (language) => {
    const model = editor?.getModel();
    if (model) {
      monaco.editor.setModelLanguage(model, language);
    }
  }
);

onBeforeUnmount(() => {
  editor?.dispose();
});
</script>

<template>
  <div ref="el" class="editor-host"></div>
</template>

<style scoped>
.editor-host {
  width: 100%;
  height: 100%;
}
</style>
