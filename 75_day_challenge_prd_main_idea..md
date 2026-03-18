# 📄 Product Requirements Document (PRD)
## Product: Discipline-Based 75-Day Challenge Tracker

---

## 1. 🧠 Product Overview

The 75-Day Challenge Tracker is a discipline-focused habit-building platform designed to help users transform their lives through structured, time-bound challenges.

Inspired by platforms like Strava (progress visibility) and LeetCode (structured progression), the product enables users to define personal goals, commit to daily tasks, and track progress with strict accountability rules.

The core philosophy is:
**Consistency + Accountability = Transformation**

---

## 2. 🎯 Objectives

### Primary Goal
Enable users to successfully complete a 75-day challenge by maintaining consistency in daily tasks.

### Secondary Goals
- Build discipline through structured constraints
- Encourage accountability through social visibility
- Provide AI-guided assistance for goal setting and improvement
- Create a system that discourages quitting and promotes commitment

---

## 3. 👤 Target Users

- Individuals seeking self-improvement (fitness, career, mental health, etc.)
- Users struggling with consistency and habit formation
- Early adopters interested in productivity and discipline systems
- Social users motivated by accountability and visibility

---

## 4. 🔑 Core Features (MVP)

### 4.1 User Authentication
- Email and password-based signup/login
- Username creation
- Persistent user sessions

### 4.2 Challenge System
- Fixed duration: 75 days
- Only one active challenge per user

#### Difficulty Levels:
- Hard → No skips allowed
- Medium → 1 skip allowed
- Soft → Up to 3 skips allowed

#### Rules:
- Users must define 5–8 daily tasks
- Challenge cannot be edited or canceled once started
- Challenge ends if failure conditions are exceeded

---

### 4.3 Task Management

Tasks categorized into:
- Health
- Spiritual
- Career
- Relationships
- Social Life
- Financial
- Personal Growth
- Family

- Tasks remain fixed throughout the challenge
- Each task must be completed daily

---

### 4.4 Daily Progress Tracking

Users can:
- View current day (e.g., Day 12/75)
- Track streak and progress
- Mark tasks as completed
- View categorized checklist

---

### 4.5 Failure & Discipline System

#### Failure Conditions:
- Missing required tasks
- Not meeting proof requirements

#### Outcomes:
- If allowed failures exceeded → FAILED
- If user accumulates 3 failures → STALE

- No restart/edit option in MVP

---

### 4.6 Proof-Based Validation

| Difficulty | Proof Requirement |
|------------|------------------|
| Hard       | Proof for all tasks |
| Medium     | Proof for at least 3 tasks |
| Soft       | Proof for at least 1 task |

- Proof submitted via image upload
- Linked to tasks per day

---

### 4.7 AI Assistant

Capabilities:
- Suggest tasks based on goals
- Analyze progress
- Chat-based guidance

---

### 4.8 Social Visibility

- Public profiles
- Story/status-based progress sharing

---

## 5. 📱 User Flow

1. User logs in
2. Views dashboard (day, streak, progress)
3. Completes tasks
4. Uploads proof
5. Receives AI feedback

---

## 6. 🧭 User States

- Active
- Completed
- Failed
- Stale

---

## 7. 🚫 Out of Scope (MVP)

- Leaderboards
- Advanced analytics
- Notifications
- Full social feed
- Gamification
- Multi-challenges

---

## 8. 💡 Product Principles

- Discipline over flexibility
- Commitment over convenience
- Clarity over complexity
- Accountability over anonymity

---

## 9. 📊 Success Metrics

- Daily Active Users
- Completion rate
- Streak length
- Retention

---

## 10. 🚀 Future Enhancements

- Leaderboards
- Advanced analytics
- AI optimization
- Social feed
- Notifications

---

## 11. 📌 Summary

This is a discipline system, not just a tracker.

Focus:
- Simplicity
- Strictness
- Commitment

Vision:
People don’t just track goals — they transform their lives.
