# **Knowledge Base: The Dynamic AI Navigator Profiler (MVP Version)**

**Version:** 1.1 (MVP) **Date:** August 6, 2025 **Status:** Revised for MVP Implementation with Pre-Generated Pairs

---

## **1.0 Core Philosophy & System Overview**

This document contains the complete methodological and psychometric foundation for the **AI Navigator Profiler MVP**. The profiler is an assessment tool designed to identify individuals with the innate psychological dispositions to excel in "AI Navigator" roles.

The core purpose is to measure stable, underlying cognitive and personality traits. For this MVP version, the test will use a fixed set of 40 pre-generated, psychometrically balanced question pairs. An LLM-powered agent will be used at the end of the assessment to provide nuanced, developmental feedback based on the user's results.

The system is guided by four principles:

* **Psychometric Rigor:** Grounded in established psychological research and committed to empirical validation.  
* **Developmental Focus:** Aims to provide actionable insights for growth, not just a label.  
* **Ethical Use:** Designed with explicit guidelines to ensure fairness, transparency, and responsible application in talent strategy.  
* **MVP Simplicity:** Prioritizes a streamlined, robust implementation to validate the core concept quickly and cost-effectively.

---

## **2.0 LLM Agent Core Operating Protocol (MVP System Prompt)**

This prompt is simplified for the MVP. The LLM's primary role is now **report generation**, not question administration.

````
You are "Navigator AI," an expert occupational psychologist and psychometrician. Your mission is to analyze a user's completed 'AI Navigator Profiler' assessment and generate an insightful, helpful, and developmental report.

## 1. Core Identity & Mission
* **Persona:** Professional, encouraging, empathetic, and strictly neutral.
* **Primary Goal:** To analyze a provided set of scores and generate a personalized report that helps the user understand their natural dispositions.
* **Anonymity:** You will be provided with anonymized data. Do not ask for, store, or reference any Personally Identifiable Information (PII).

## 2. Phase 1: Assessment Administration (Handled by Application Logic)
The user will have already completed a 40-item assessment consisting of pre-generated pairs. You are not involved in asking the questions.

## 3. Phase 2: Reporting and Feedback Generation (Your Task)
You will be given the final scores for a user across the 11 constructs and 3 archetypes. Your task is to generate a comprehensive report based on this data.

### **Report Structure & Tone:**
* **Tone:** The report must be **empowering, constructive, and forward-looking.** Avoid definitive or clinical labels. Use phrases like "Your profile suggests a preference for..." or "You have a tendency to..." instead of "You are...".
* **Format:** Generate the report using the following Markdown template, filling in the bracketed sections with personalized content based on the user's unique score profile.

```markdown
# Your AI Navigator Profile

**Nickname:** [Insert User's Nickname provided by the system]

### Executive Summary

[Generate 2-3 sentences of nuanced interpretation based on the user's mix of primary and secondary archetypes. Example: "Your profile highlights a powerful blend of the Critical Interrogator and Curious Experimenter, suggesting you pair rigorous analysis with a hands-on, exploratory drive."]

---

### Your Primary Archetype: [Insert Primary Archetype Name]

[Insert the Core Description for the primary archetype from your knowledge base.]

**Signature Strengths:**
* [List strengths for the primary archetype]

**Potential Blind Spots:**
* [List blind spots for the primary archetype]

---

### Developmental Opportunities

* **To enhance your [Primary Archetype] style:** [Provide 1-2 sentences of actionable advice based on the archetype's blind spots.]
* **To leverage your [Secondary Archetype] strengths:** [Provide 1-2 sentences of actionable advice on how to integrate the secondary archetype's strengths.]

---

### Detailed Trait Scores

[The application will render the list of the 11 constructs and their percentile scores here.]
````

````

---

## **3.0 Psychometric Framework: The 11 Constructs**
_(This section remains unchanged from the previous version, defining NFC, AOT, EC, TOA, IH, Trait EI, Holistic Thinking, Experimental Drive, Deliberative Stance, Principled Ethics, and General Trust.)_

---

## **4.0 The AI Navigator Archetypes**
_(This section remains unchanged, defining The Critical Interrogator, The Human-Centric Strategist, and The Curious Experimenter, including their formulas, strengths, and blind spots.)_

---

## **5.0 Assessment Logic & Scoring (MVP Version)**

* **Item Pairing Logic:** The test uses a **fixed list of 40 pre-generated pairs** from the `[PRE-GENERATED PAIRS]` section of the knowledge base. These pairs were created offline by an expert panel to ensure they are psychometrically balanced, matching statements with similar `social_desirability_score`.
* **Scoring Algorithm:**
    1.  **Raw Score:** For each of the 11 constructs, sum the number of times the user chose a statement coded to that construct.
    2.  **Weighted Score:** Apply an empirically-derived weight to each raw score. (Note: For the MVP, all weights will be `1.0`).
    3.  **Archetype Score:** Sum the relevant weighted scores according to the archetype formulas.
* **Norming Principles:** All final scores must be converted to percentiles based on a relevant norm group. A score's meaning comes from its comparison to this group, not from its absolute value.

---

## **6.0 Reporting & Feedback Generation Protocol**
_(This section is now primarily encapsulated within the LLM prompt in Section 2.0. It defines the structure and tone for the dynamically generated report.)_

---

## **7.0 Pre-Generated Pairs & Item Bank (MVP Version)**

This section defines the fixed 40-item test and the reference library of all statements.

### **7.1 Pre-Generated Question Pairs**
This is the definitive list of 40 questions for the profiler. The application will serve them in this order.

```yaml
question_pairs:
  - pair_id: 1
    statement_1_id: 103 # NFC (6.4)
    statement_2_id: 604 # Trait EI (6.4)
  - pair_id: 2
    statement_1_id: 204 # AOT (7.0)
    statement_2_id: 1003 # Principled Ethics (7.0)
  - pair_id: 3
    statement_1_id: 303 # EC (6.5)
    statement_2_id: 902 # Deliberative Stance (6.5)
  - pair_id: 4
    statement_1_id: 401 # TOA (5.6)
    statement_2_id: 804 # Experimental Drive (5.6)
  - pair_id: 5
    statement_1_id: 505 # IH (6.9)
    statement_2_id: 1002 # Principled Ethics (6.9)
  - pair_id: 6
    statement_1_id: 602 # Trait EI (6.7)
    statement_2_id: 203 # AOT (6.7)
  - pair_id: 7
    statement_1_id: 704 # Holistic Thinking (6.3)
    statement_2_id: 305 # EC (6.3)
  - pair_id: 8
    statement_1_id: 1104 # General Trust (6.0)
    statement_2_id: 805 # Experimental Drive (6.0)
  - pair_id: 9
    statement_1_id: 901 # Deliberative Stance (6.3)
    statement_2_id: 601 # Trait EI (6.3)
  - pair_id: 10
    statement_1_id: 504 # IH (6.8)
    statement_2_id: 1001 # Principled Ethics (6.8)
  - pair_id: 11
    statement_1_id: 104 # NFC (6.2)
    statement_2_id: 302 # EC (6.2)
  - pair_id: 12
    statement_1_id: 201 # AOT (6.8)
    statement_2_id: 504 # IH (6.8)
  - pair_id: 13
    statement_1_id: 404 # TOA (5.9)
    statement_2_id: 102 # NFC (5.9)
  - pair_id: 14
    statement_1_id: 802 # Experimental Drive (5.7)
    statement_2_id: 1105 # General Trust (5.7)
  - pair_id: 15
    statement_1_id: 701 # Holistic Thinking (6.2)
    statement_2_id: 903 # Deliberative Stance (6.1)
  - pair_id: 16
    statement_1_id: 605 # Trait EI (6.5)
    statement_2_id: 503 # IH (6.5)
  - pair_id: 17
    statement_1_id: 301 # EC (6.4)
    statement_2_id: 703 # Holistic Thinking (6.4)
  - pair_id: 18
    statement_1_id: 1004 # Principled Ethics (6.7)
    statement_2_id: 602 # Trait EI (6.7)
  - pair_id: 19
    statement_1_id: 202 # AOT (6.9)
    statement_2_id: 505 # IH (6.9)
  - pair_id: 20
    statement_1_id: 403 # TOA (6.1)
    statement_2_id: 705 # Holistic Thinking (6.1)
  - pair_id: 21
    statement_1_id: 105 # NFC (5.7)
    statement_2_id: 405 # TOA (5.7)
  - pair_id: 22
    statement_1_id: 801 # Experimental Drive (5.5)
    statement_2_id: 1102 # General Trust (5.4)
  - pair_id: 23
    statement_1_id: 905 # Deliberative Stance (6.6)
    statement_2_id: 502 # IH (6.6)
  - pair_id: 24
    statement_1_id: 1005 # Principled Ethics (6.6)
    statement_2_id: 205 # AOT (6.6)
  - pair_id: 25
    statement_1_id: 303 # EC (6.5)
    statement_2_id: 605 # Trait EI (6.5)
  - pair_id: 26
    statement_1_id: 702 # Holistic Thinking (6.0)
    statement_2_id: 304 # EC (6.0)
  - pair_id: 27
    statement_1_id: 103 # NFC (6.4)
    statement_2_id: 904 # Deliberative Stance (6.4)
  - pair_id: 28
    statement_1_id: 501 # IH (6.7)
    statement_2_id: 1004 # Principled Ethics (6.7)
  - pair_id: 29
    statement_1_id: 201 # AOT (6.8)
    statement_2_id: 504 # IH (6.8)
  - pair_id: 30
    statement_1_id: 402 # TOA (5.3)
    statement_2_id: 803 # Experimental Drive (5.2)
  - pair_id: 31
    statement_1_id: 1103 # General Trust (5.9)
    statement_2_id: 102 # NFC (5.9)
  - pair_id: 32
    statement_1_id: 603 # Trait EI (6.1)
    statement_2_id: 903 # Deliberative Stance (6.1)
  - pair_id: 33
    statement_1_id: 703 # Holistic Thinking (6.4)
    statement_2_id: 604 # Trait EI (6.4)
  - pair_id: 34
    statement_1_id: 305 # EC (6.3)
    statement_2_id: 901 # Deliberative Stance (6.3)
  - pair_id: 35
    statement_1_id: 105 # NFC (5.7)
    statement_2_id: 1105 # General Trust (5.7)
  - pair_id: 36
    statement_1_id: 205 # AOT (6.6)
    statement_2_id: 905 # Deliberative Stance (6.6)
  - pair_id: 37
    statement_1_id: 805 # Experimental Drive (6.0)
    statement_2_id: 1104 # General Trust (6.0)
  - pair_id: 38
    statement_1_id: 405 # TOA (5.7)
    statement_2_id: 802 # Experimental Drive (5.7)
  - pair_id: 39
    statement_1_id: 1001 # Principled Ethics (6.8)
    statement_2_id: 201 # AOT (6.8)
  - pair_id: 40
    statement_1_id: 503 # IH (6.5)
    statement_2_id: 303 # EC (6.5)
````

### **7.2 Item Bank Reference**

This library contains all individual statements, referenced by the `Pre-Generated Question Pairs` list.

```
item_bank:
  - {item_id: 101, statement_text: "I enjoy the process of abstract or philosophical thinking.", construct: "Need for Cognition", social_desirability_score: 5.8}
  - {item_id: 102, statement_text: "I get more satisfaction from a challenging mental task than an easy one.", construct: "Need for Cognition", social_desirability_score: 5.9}
  - {item_id: 103, statement_text: "I like to analyze a problem from every angle before making a decision.", construct: "Need for Cognition", social_desirability_score: 6.4}
  - {item_id: 104, statement_text: "I am drawn to tasks that require me to think deeply and concentrate.", construct: "Need for Cognition", social_desirability_score: 6.2}
  - {item_id: 105, statement_text: "I would rather do something that requires a lot of thought than something that is simple.", construct: "Need for Cognition", social_desirability_score: 5.7}
  - {item_id: 201, statement_text: "I enjoy listening to arguments that challenge my current point of view.", construct: "Actively Open-Minded Thinking", social_desirability_score: 6.8}
  - {item_id: 202, statement_text: "I actively look for evidence that might contradict my existing beliefs.", construct: "Actively Open-Minded Thinking", social_desirability_score: 6.9}
  - {item_id: 203, statement_text: "I think it is important to expose myself to opinions I strongly disagree with.", construct: "Actively Open-Minded Thinking", social_desirability_score: 6.7}
  - {item_id: 204, statement_text: "I am willing to change my mind on an important issue when presented with a good argument.", construct: "Actively Open-Minded Thinking", social_desirability_score: 7.0}
  - {item_id: 205, statement_text: "I consider critiques of my ideas as a valuable opportunity to improve them.", construct: "Actively Open-Minded Thinking", social_desirability_score: 6.6}
  - {item_id: 301, statement_text: "When I find a topic interesting, I feel a strong desire to learn everything about it.", construct: "Epistemic Curiosity", social_desirability_score: 6.4}
  - {item_id: 302, statement_text: "The feeling of 'not knowing' something motivates me to find an answer.", construct: "Epistemic Curiosity", social_desirability_score: 6.2}
  - {item_id: 303, statement_text: "I love learning new things just for the sake of learning.", construct: "Epistemic Curiosity", social_desirability_score: 6.5}
  - {item_id: 304, statement_text: "If I hear a new term or concept, I'll often look it up immediately.", construct: "Epistemic Curiosity", social_desirability_score: 6.0}
  - {item_id: 305, statement_text: "I have a wide range of interests and am curious about many things.", construct: "Epistemic Curiosity", social_desirability_score: 6.3}
  - {item_id: 401, statement_text: "I am comfortable moving forward on a project even if all the details aren't finalized.", construct: "Tolerance for Ambiguity", social_desirability_score: 5.6}
  - {item_id: 402, statement_text: "I prefer jobs where my day-to-day tasks are varied and unpredictable.", construct: "Tolerance for Ambiguity", social_desirability_score: 5.3}
  - {item_id: 403, statement_text: "Unexpected changes to a plan don't typically fluster me.", construct: "Tolerance for Ambiguity", social_desirability_score: 6.1}
  - {item_id: 404, statement_text: "I can function well in situations where the rules are not clearly defined.", construct: "Tolerance for Ambiguity", social_desirability_score: 5.9}
  - {item_id: 405, statement_text: "I find it energizing to work on problems where the final outcome is not yet clear.", construct: "Tolerance for Ambiguity", social_desirability_score: 5.7}
  - {item_id: 501, statement_text: "I readily accept that my own beliefs could be wrong.", construct: "Intellectual Humility", social_desirability_score: 6.7}
  - {item_id: 502, statement_text: "I'm quick to admit when a task is beyond my current expertise.", construct: "Intellectual Humility", social_desirability_score: 6.6}
  - {item_id: 503, statement_text: "I am aware that my own knowledge is limited and incomplete.", construct: "Intellectual Humility", social_desirability_score: 6.5}
  - {item_id: 504, statement_text: "I am comfortable saying 'I don't know' in a professional setting.", construct: "Intellectual Humility", social_desirability_score: 6.8}
  - {item_id: 505, statement_text: "I can listen to criticism about my ideas without getting defensive.", construct: "Intellectual Humility", social_desirability_score: 6.9}
  - {item_id: 601, statement_text: "I am good at sensing what others are feeling, even if they don't say it.", construct: "Trait Emotional Intelligence", social_desirability_score: 6.3}
  - {item_id: 602, statement_text: "I'm good at staying calm under pressure.", construct: "Trait Emotional Intelligence", social_desirability_score: 6.7}
  - {item_id: 603, statement_text: "I'm often the person others come to for emotional support or advice.", construct: "Trait Emotional Intelligence", social_desirability_score: 6.1}
  - {item_id: 604, statement_text: "I find it easy to connect with people from different backgrounds.", construct: "Trait Emotional Intelligence", social_desirability_score: 6.4}
  - {item_id: 605, statement_text: "I am sensitive to the emotional needs of my colleagues.", construct: "Trait Emotional Intelligence", social_desirability_score: 6.5}
  - {item_id: 701, statement_text: "I like to understand the big picture before diving into the individual components.", construct: "Holistic Thinking Preference", social_desirability_score: 6.2}
  - {item_id: 702, statement_text: "I often think about how small changes can impact the entire system.", construct: "Holistic Thinking Preference", social_desirability_score: 6.0}
  - {item_id: 703, statement_text: "When planning, I think about the ripple effects of a decision.", construct: "Holistic Thinking Preference", social_desirability_score: 6.4}
  - {item_id: 704, statement_text: "To solve a problem, I first try to understand its context and relationships.", construct: "Holistic Thinking Preference", social_desirability_score: 6.3}
  - {item_id: 705, statement_text: "I naturally look for how different pieces of a project connect with each other.", construct: "Holistic Thinking Preference", social_desirability_score: 6.1}
  - {item_id: 801, statement_text: "My first instinct with a new tool is to start playing with it to see how it works.", construct: "Experimental Drive", social_desirability_score: 5.5}
  - {item_id: 802, statement_text: "I learn best by trying things out for myself.", construct: "Experimental Drive", social_desirability_score: 5.7}
  - {item_id: 803, statement_text: "I enjoy taking things apart to understand how they work.", construct: "Experimental Drive", social_desirability_score: 5.2}
  - {item_id: 804, statement_text: "I'd rather build a quick prototype than spend a long time on a theoretical design.", construct: "Experimental Drive", social_desirability_score: 5.6}
  - {item_id: 805, statement_text: "I like to experiment with different approaches to find the best one.", construct: "Experimental Drive", social_desirability_score: 6.0}
  - {item_id: 901, statement_text: "I tend to pause and think things through rather than relying on my gut instinct.", construct: "Deliberative Stance", social_desirability_score: 6.3}
  - {item_id: 902, statement_text: "I double-check my reasoning before committing to a final answer.", construct: "Deliberative Stance", social_desirability_score: 6.5}
  - {item_id: 903, statement_text: "I am more of a reflective person than an impulsive one.", construct: "Deliberative Stance", social_desirability_score: 6.1}
  - {item_id: 904, statement_text: "My gut feelings are something I check with logic, not something I blindly follow.", construct: "Deliberative Stance", social_desirability_score: 6.4}
  - {item_id: 905, statement_text: "I prefer to carefully consider all options before making a choice.", construct: "Deliberative Stance", social_desirability_score: 6.6}
  - {item_id: 1001, statement_text: "I feel it's important to stick to principles of fairness, even if it makes things difficult.", construct: "Principled Ethics Orientation", social_desirability_score: 6.8}
  - {item_id: 1002, statement_text: "Doing the right thing is more important to me than being popular.", construct: "Principled Ethics Orientation", social_desirability_score: 6.9}
  - {item_id: 1003, statement_text: "I believe that rules of fairness should apply to everyone equally, without exception.", construct: "Principled Ethics Orientation", social_desirability_score: 7.0}
  - {item_id: 1004, statement_text: "I hold my ethical standards regardless of what others are doing.", construct: "Principled Ethics Orientation", social_desirability_score: 6.7}
  - {item_id: 1005, statement_text: "An unfair outcome for others is something I work hard to prevent.", construct: "Principled Ethics Orientation", social_desirability_score: 6.6}
  - {item_id: 1101, statement_text: "I tend to trust new colleagues until I have a reason not to.", construct: "General Trust Propensity", social_desirability_score: 5.8}
  - {item_id: 1102, statement_text: "I generally assume people are telling the truth.", construct: "General Trust Propensity", social_desirability_score: 5.4}
  - {item_id: 1103, statement_text: "I find it easy to place my trust in others on a team.", construct: "General Trust Propensity", social_desirability_score: 5.9}
  - {item_id: 1104, statement_text: "I assume that my coworkers are competent and reliable.", construct: "General Trust Propensity", social_desirability_score: 6.0}
  - {item_id: 1105, statement_text: "I prefer to rely on the goodwill of others rather than being suspicious.", construct: "General Trust Propensity", social_desirability_score: 5.7}
```

