import React from "react";
import ReactMarkdown from "react-markdown";

interface Props {
  markdown: string;
  chunks: { chunk_id: string; text: string }[];
}

export default function SidePanel({ markdown, chunks }: Props) {
  // UUIDが含まれるチャンクのtextをspanで囲む
  let rendered = markdown;
  chunks.forEach(({ chunk_id, text }) => {
    const escaped = text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(escaped, "g");
    rendered = rendered.replace(regex, `<span id="${chunk_id}">${text}</span>`);
  });

  return (
    <div className="border-l overflow-y-scroll p-6 text-sm whitespace-pre-wrap bg-gray-50">
      <ReactMarkdown
        components={{
          span: ({ node, ...props }) => (
            <span {...props} className="transition-colors duration-300" />
          ),
        }}
      >
        {rendered}
      </ReactMarkdown>
    </div>
  );
}