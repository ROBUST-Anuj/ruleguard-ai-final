# RuleGuard — Documented Contradictions

This document records the three deliberate contradictions planted in the NIT policy corpus. Each contradiction involves provisions from different documents that create genuine conflicts when applied to overlapping situations.

---

## CON-001: Attendance Threshold for Medical Exemption

### Documents Involved
- **Document A:** `attendance_policy.md` — Section 4.2
- **Document B:** `medical_exemption_policy.md` — Section 3.1

### Exact Conflicting Text

**Provision A** (attendance_policy.md, Section 4.2):
> "Students must maintain a minimum attendance of 75% in each registered course to be eligible for appearing in the semester-end examinations. No exceptions shall be granted below this threshold."

**Provision B** (medical_exemption_policy.md, Section 3.1):
> "Students who submit an approved medical exemption certificate from the NIT Health Centre or a recognized hospital may be permitted to appear for semester-end examinations with attendance as low as 60%, subject to approval by the Dean of Academic Affairs."

### Explanation
The Attendance Policy explicitly states that the 75% threshold admits "no exceptions." However, the Medical Exemption Policy creates an exception by allowing students with approved medical certificates to appear for examinations with attendance as low as 60%. These provisions directly conflict because one categorically prohibits what the other explicitly permits. A student with 68% attendance and a medical certificate would be eligible under the Medical Exemption Policy but ineligible under the Attendance Policy.

### Example Question That Should Trigger This Contradiction
> "Can a student with 68% attendance and an approved medical certificate appear for the semester examination?"

---

## CON-002: Fee Payment Deadline and Deregistration

### Documents Involved
- **Document A:** `fee_regulations.md` — Section 2.1
- **Document B:** `academic_regulations.md` — Section 6.3

### Exact Conflicting Text

**Provision A** (fee_regulations.md, Section 2.1):
> "All semester tuition fees must be paid on or before September 15 of the academic year for the Autumn Semester. Failure to pay by this date will result in automatic deregistration from all courses."

**Provision B** (academic_regulations.md, Section 6.3):
> "Students may complete fee payment until September 20 without any academic penalty. Course registration shall remain valid during this grace period."

### Explanation
The Fee Regulations state that non-payment by September 15 triggers "automatic deregistration from all courses." However, the Academic Regulations state that students may pay until September 20 without penalty and that "course registration shall remain valid" during this period. These provisions conflict because a student who has not paid by September 16 would be automatically deregistered under the Fee Regulations but would still have valid registration under the Academic Regulations. The two documents disagree on whether there is a grace period between September 15 and September 20.

### Example Question That Should Trigger This Contradiction
> "If I haven't paid my tuition fee by September 16, will my course registration be cancelled?"

---

## CON-003: Number of Supplementary Examination Attempts

### Documents Involved
- **Document A:** `examination_policy.md` — Section 7.1
- **Document B:** `academic_regulations.md` — Section 5.4

### Exact Conflicting Text

**Provision A** (examination_policy.md, Section 7.1):
> "A student who fails a course shall be permitted to appear for exactly one supplementary examination for that course. No further supplementary attempts shall be allowed."

**Provision B** (academic_regulations.md, Section 5.4):
> "Students who fail a supplementary examination may apply for a second supplementary attempt, provided they have a cumulative GPA of 5.0 or above and the course is a core/mandatory course. The second supplementary examination shall be conducted during the next regular examination cycle."

### Explanation
The Examination Policy categorically states that only "exactly one" supplementary examination is permitted and that "no further supplementary attempts shall be allowed." The Academic Regulations, however, provide for a second supplementary attempt under certain conditions (CGPA ≥ 5.0 and core course). These provisions conflict because one absolutely prohibits additional attempts while the other conditionally allows them. A student who failed a supplementary examination in a core course with a CGPA of 5.0 would be eligible for a second attempt under the Academic Regulations but categorically denied under the Examination Policy.

### Example Question That Should Trigger This Contradiction
> "Can a student with a CGPA of 5.5 who failed the supplementary exam in a core course apply for a second supplementary attempt?"

---

## Summary

| ID | Topic | Document A | Document B | Conflict |
|----|-------|-----------|-----------|----------|
| CON-001 | Attendance/Medical | attendance_policy.md §4.2 | medical_exemption_policy.md §3.1 | 75% with no exceptions vs. 60% with medical certificate |
| CON-002 | Fee Deadline | fee_regulations.md §2.1 | academic_regulations.md §6.3 | Auto-deregistration after Sep 15 vs. grace period until Sep 20 |
| CON-003 | Supplementary Exams | examination_policy.md §7.1 | academic_regulations.md §5.4 | Exactly one attempt vs. second attempt for core courses |
