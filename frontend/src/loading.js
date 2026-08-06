import { ref } from "vue";

export const pageLoading = ref(false);

export function startPageLoading() {
  pageLoading.value = true;
}

export function stopPageLoading() {
  pageLoading.value = false;
}
