function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

const LABEL_LINE = /^(示例\s*\d+[：:]|输入[：:]|输出[：:]|（无输入）)/;

export function formatRichText(text) {
  if (!text) return "";
  return String(text)
    .split("\n")
    .map((line) => {
      let html = escapeHtml(line);
      if (LABEL_LINE.test(line.trim())) {
        html = `<strong>${html}</strong>`;
      }
      return html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
    })
    .join("<br>");
}
