---
type: learning-course-home
topic: "{{TOPIC}}"
subject: "{{SUBJECT}}"
course_id: "{{COURSE_ID}}"
created: "{{DATE}}"
updated: "{{DATE}}"
timezone: "{{TIMEZONE}}"
status: active
---

# {{TOPIC}}

<!-- AI-MANAGED:START -->
## 学习使命
- 最终目标：
- 真实应用或考试目标：
- 完成标准：能解释、辨析、应用、迁移、纠错，并完成约定的综合任务。

## 当前状态
- 当前知识点：
- 当前阶段：初始化
- 下一步：导入资料并建立知识点地图。

## 资料范围
- 待登记于 [[01-原始资料]]

## 导航
- [[02-知识点地图]]
- [[03-掌握度账本]]
- [[04-错题与误区]]
- [[05-作业与项目]]
- [[06-复习队列]]

## 未解决问题
- 
<!-- AI-MANAGED:END -->

## 我的私有笔记（AI 默认不修改）
- 

## 动态视图 (Dataview)
### 最近学习会话
```dataview
TABLE date AS "日期", session_count AS "会话数", updated AS "更新时间"
FROM ""
WHERE topic = "{{TOPIC}}" AND type = "learning-session"
SORT date DESC
LIMIT 5
```
