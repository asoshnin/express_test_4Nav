# **Methodology: The AI Navigator Express Profiler**

# **1\. Introduction & Purpose**

This document provides the complete methodology for the **AI Navigator Express Profiler**, an online psychometric instrument designed for the rapid screening of candidates for AI Navigator roles.

The profiler's purpose is to measure the underlying psychological dispositions that indicate a candidate's innate potential to excel at collaborating with, critically challenging, and translating the outputs of artificial intelligence systems. It is designed as a scalable, efficient, and insightful first-pass assessment to identify high-potential individuals for more in-depth evaluation.

The core philosophy is to measure stable personality preferences and cognitive styles rather than perishable technical skills. It uses a forced-choice format to mitigate common survey biases and reveal a candidate's authentic motivational hierarchy.

# **2\. Psychometric Framework: Measured Constructs**

The profiler assesses eleven psychological constructs derived from the Daedalus Protocol research. These constructs are measured through a self-report format and represent stable traits that predict success in AI navigation work. All eleven constructs are measured directly through validated self-report items:

1. **Need for Cognition (NFC):** The intrinsic motivation to engage in and enjoy effortful cognitive activities.  
2. **Actively Open-Minded Thinking (AOT):** The willingness to seek out and thoughtfully consider evidence that contradicts one's own beliefs.  
3. **Epistemic Curiosity (EC):** The desire for new knowledge, encompassing both the joy of discovery and the drive to resolve knowledge gaps.  
4. **Tolerance for Ambiguity (TOA):** The ability to perceive and manage uncertain, complex, or novel situations without psychological distress.  
5. **Intellectual Humility (IH):** A non-threatening awareness of one's intellectual fallibility and an openness to being wrong.  
6. **Trait Emotional Intelligence (Trait EI):** A constellation of emotional self-perceptions, including empathy, assertiveness, and stress management.  
7. **Holistic Thinking Preference (HTP):** A preference for understanding problems by examining interconnections, feedback loops, and the system as a whole, rather than focusing on isolated, linear cause-and-effect chains.  
8. **Experimental Drive (ED):** An innate drive toward hands-on exploration, experimentation, and learning through iterative trial-and-error.  
9. **Deliberative Stance (DS):** A preference for overriding an initial intuitive response to engage in more effortful, reflective, and logical analysis.  
10. **Principled Ethics Orientation (PEO):** An orientation toward making decisions based on universal principles of fairness and justice, rather than solely on rules, authority, or self-interest.  
11. **General Trust Propensity (GTP):** A general, trait-based willingness to trust others and accept vulnerability in social situations.

# **3\. Assessment Implementation: The Online Tool**

The profiler is implemented as a simple, web-based assessment tool.

* **User Interface:** The interface is clean, minimalist, and mobile-friendly. Each screen presents a single question with a progress bar visible to manage candidate expectations.  
* **Format:** **40 forced-choice item pairs.** Each item presents two distinct statements (Statement A and Statement B).  
* **Task:** The candidate must choose the statement that is "More like me." There is no neutral option.  
* **Instructions:** Clear instructions at the start state:  
  * The assessment is untimed but should take approximately 10-15 minutes.  
  * There are no right or wrong answers.  
  * Candidates should go with their first instinct and not overthink their choices.  
  * The goal is to understand their natural preferences and work style.  
* **Data Capture:** The system records the candidate's choice for each of the 40 items. Each statement (A or B) within an item pair is pre-coded to correspond to one of the 11 psychometric constructs.

# **4\. Scoring Algorithm**

The scoring process involves three automated steps to convert raw choices into a final profile.

## **Step 1: Raw Score Calculation**

For each of the 11 constructs, a raw score is calculated by summing the number of times the candidate chose a statement pre-coded to that construct.

* **Formula:** Raw Score (Construct X) \= Σ (Choices for Construct X)  
* **Example:** If a candidate chooses 5 statements corresponding to Need for Cognition (NFC) across the 40 items, the Raw Score (NFC) \= 5\.

## **Step 2: Archetype Score Calculation**

The 11 raw construct scores are aggregated into three distinct AI Navigator Archetype scores using the following formulas:

* **Archetype 1: The Critical Interrogator**  
  * **Formula:** Score (Interrogator) \= Raw Score (NFC) \+ Raw Score (AOT) \+ Raw Score (EC) \+ Raw Score (IH) \+ Raw Score (DS)  
* **Archetype 2: The Human-Centric Strategist**  
  * **Formula:** Score (Strategist) \= Raw Score (Trait EI) \+ Raw Score (HTP) \+ Raw Score (PEO) \+ Raw Score (GTP)  
* **Archetype 3: The Curious Experimenter**  
  * **Formula:** Score (Experimenter) \= Raw Score (TOA) \+ Raw Score (ED) \+ Raw Score (EC) \+ Raw Score (AOT)

*Note: Epistemic Curiosity (EC) and Actively Open-Minded Thinking (AOT) contribute to both the Interrogator and Experimenter profiles, reflecting their dual importance in analytical rigor and exploratory learning.*

## **Step 3: Final Profile Determination**

The candidate's primary AI Navigator Style is determined by identifying the archetype with the highest total score.

* **Logic:** Primary Profile \= MAX(Score(Interrogator), Score(Strategist), Score(Experimenter))

# **5\. Profile Interpretation & Reporting**

The final output is a dynamically generated report that presents the candidate's primary AI Navigator Style.

* **The Critical Interrogator**  
  * **Description:** This individual is a rigorous, analytical thinker driven to find the most accurate answer. They are defined by their propensity to challenge assumptions—both their own and the AI's.  
  * **Signature Strengths:** Excels at identifying flaws in AI outputs, combating confirmation bias, ensuring analytical integrity, and navigating ethical complexities with a principled approach.  
* **The Human-Centric Strategist**  
  * **Description:** This individual excels at bridging the gap between computational insights and real-world human systems. They are defined by their ability to build trust, communicate effectively, and translate data into wise, contextualized action.  
  * **Signature Strengths:** Excels at stakeholder management, communicating high-stakes information with empathy, fostering collaboration, and anticipating the broader organizational impact of AI-driven decisions.  
* **The Curious Experimenter**  
  * **Description:** This individual is a natural explorer and hands-on learner, motivated by a drive to understand how complex systems work. They are defined by their comfort with uncertainty and their proactive, experimental approach to developing technical fluency.  
  * **Signature Strengths:** Excels at rapidly learning new AI tools, discovering novel applications, troubleshooting opaque systems through trial-and-error, and maintaining effectiveness in ambiguous, fast-changing environments.

The report clearly states the candidate's primary profile and may also mention secondary inclinations if another archetype score is close to the primary one, providing a nuanced view of their potential.

# **6\. Technical Implementation Notes**

* **Construct Distribution:** Each of the 11 constructs is represented by 5 unique statement IDs (e.g., 101-105 for Need for Cognition), ensuring balanced measurement across all constructs.  
* **Question Pair Design:** Each of the 40 question pairs presents two statements from different constructs, ensuring forced-choice decisions that reveal authentic preferences.  
* **Scoring Simplicity:** The current implementation uses unweighted raw scores avoiding the complexity of norm-based weighting systems.  
* **Percentile Calculation:** A simplified percentile calculation is used based on the maximum possible score (40), providing a relative performance indicator.