// Western University Textbook Typst Template
// Designed for "AI Research Chronicle & Paradigm Flows (2023–2026)"

#let navy = rgb("#13294B")
#let royal = rgb("#1F4E79")
#let crimson = rgb("#B84A39")
#let gold = rgb("#C98A2C")
#let teal = rgb("#2E7D6B")
#let ivory = rgb("#FAF8F4")
#let ink = rgb("#1E293B")
#let muted = rgb("#64748B")

#let body_fonts = ("Georgia", "Libertinus Serif", "Songti SC", "STSong", "Noto Serif CJK SC")
#let sans_fonts = ("Helvetica Neue", "Arial", "Hiragino Sans GB", "Heiti SC", "Noto Sans CJK SC")
#let mono_fonts = ("Menlo", "DejaVu Sans Mono", "Noto Sans Mono CJK SC")

#let current_chapter = state("current_chapter", "前言与导读")

#let learning_box(body) = block(
  width: 100%,
  fill: rgb("#EEF4FA"),
  stroke: (left: 4pt + navy, top: 0.6pt + rgb("#CBD5E1"), right: 0.6pt + rgb("#CBD5E1"), bottom: 0.6pt + rgb("#CBD5E1")),
  radius: (right: 4pt),
  inset: (x: 14pt, y: 12pt),
  above: 14pt,
  below: 16pt,
  breakable: true,
)[
  #text(font: sans_fonts, size: 9pt, weight: "bold", fill: navy, tracking: 0.8pt)[LEARNING OBJECTIVES · 本章学习目标]
  #v(5pt)
  #set text(size: 9.6pt, fill: rgb("#1E293B"))
  #body
]

#let concept_box(title, body) = block(
  width: 100%,
  fill: rgb("#F4F7FB"),
  stroke: (left: 3.8pt + royal, rest: 0.5pt + rgb("#D5DFEC")),
  radius: (right: 4pt),
  inset: (x: 14pt, y: 11pt),
  above: 13pt,
  below: 14pt,
  breakable: true,
)[
  #text(font: sans_fonts, size: 8.8pt, weight: "bold", fill: royal, tracking: 0.6pt)[KEY CONCEPT · 核心概念]
  #if title != "" [
    #h(6pt)
    #text(font: sans_fonts, size: 9.8pt, weight: "bold", fill: navy)[— #title]
  ]
  #v(5pt)
  #set text(size: 9.5pt)
  #body
]

#let landmark_box(title, body) = block(
  width: 100%,
  fill: rgb("#FBF8F2"),
  stroke: (left: 3.8pt + crimson, rest: 0.6pt + rgb("#E6D7CC")),
  radius: (right: 4pt),
  inset: (x: 14pt, y: 11pt),
  above: 14pt,
  below: 15pt,
  breakable: true,
)[
  #text(font: sans_fonts, size: 8.8pt, weight: "bold", fill: crimson, tracking: 0.6pt)[LANDMARK STUDY · 里程碑论文精读]
  #if title != "" [
    #v(3pt)
    #text(font: sans_fonts, size: 10pt, weight: "bold", fill: navy)[#title]
  ]
  #v(5pt)
  #set text(size: 9.4pt)
  #body
]

#let shift_box(title, body) = block(
  width: 100%,
  fill: rgb("#FDF7EC"),
  stroke: (left: 3.8pt + gold, rest: 0.6pt + rgb("#EAD8B8")),
  radius: (right: 4pt),
  inset: (x: 14pt, y: 11pt),
  above: 14pt,
  below: 15pt,
  breakable: true,
)[
  #text(font: sans_fonts, size: 8.8pt, weight: "bold", fill: gold, tracking: 0.6pt)[PARADIGM SHIFT · 范式跃迁洞察]
  #if title != "" [
    #h(6pt)
    #text(font: sans_fonts, size: 9.8pt, weight: "bold", fill: navy)[— #title]
  ]
  #v(5pt)
  #set text(size: 9.5pt)
  #body
]

#let landmark_card(rank, title, meta_line, perspective, experiments, conclusions, takeaway) = block(
  width: 100%,
  fill: rgb("#FCFBF8"),
  stroke: (left: 3pt + royal, rest: 0.5pt + rgb("#DDD6C8")),
  radius: 3pt,
  inset: (x: 11pt, y: 9pt),
  above: 8pt,
  below: 9pt,
  breakable: true,
)[
  #text(font: sans_fonts, size: 9.8pt, weight: "bold", fill: navy)[#rank. #title]
  #v(2pt)
  #text(font: sans_fonts, size: 8.4pt, fill: muted)[#meta_line]
  #v(4pt)
  #set text(size: 9pt)
  #set par(leading: 0.68em, spacing: 0.5em)
  - *核心观点*：#perspective
  - *方法与实验*：#experiments
  - *实验结论*：#conclusions
  - *Takeaway*：#takeaway
]

#let textbook_figure(img_path, cap_text) = figure(
  block(
    width: 100%,
    inset: 2pt,
    image(img_path, width: 100%),
  ),
  supplement: none,
  caption: text(font: sans_fonts, size: 8.8pt, fill: muted)[#cap_text],
  gap: 7pt,
)

#let part_divider(part_label, title_zh, title_en, summary_text) = {
  pagebreak(weak: true)
  page(header: none, footer: none, fill: rgb("#F6F4EE"))[
    #v(1.6fr)
    #block(
      width: 100%,
      stroke: (left: 6pt + crimson),
      inset: (left: 18pt, y: 8pt),
    )[
      #text(font: sans_fonts, size: 12pt, weight: "bold", fill: crimson, tracking: 2pt)[#part_label]
      #v(8pt)
      #text(font: sans_fonts, size: 25pt, weight: "bold", fill: navy)[#title_zh]
      #v(6pt)
      #text(font: body_fonts, style: "italic", size: 13.5pt, fill: royal)[#title_en]
    ]
    #v(18pt)
    #line(length: 100%, stroke: 0.8pt + rgb("#C8C1B4"))
    #v(14pt)
    #block(width: 92%)[
      #set text(font: body_fonts, size: 10.6pt, fill: ink)
      #set par(leading: 0.95em)
      #summary_text
    ]
    #v(2.4fr)
  ]
}

#let chapter_start(chap_badge, heading_title) = {
  pagebreak(weak: true)
  current_chapter.update(heading_title)
  block(width: 100%, below: 16pt)[
    #text(font: sans_fonts, size: 9.5pt, weight: "bold", fill: crimson, tracking: 1.8pt)[#chap_badge]
    #v(4pt)
    #heading(level: 1)[#heading_title]
    #v(6pt)
    #line(length: 100%, stroke: 1.8pt + navy)
    #v(2pt)
    #line(length: 36%, stroke: 2.5pt + gold)
  ]
}
