# Contribution of Team Members

Project: Numerical Reasoning over Financial Reports
Course: Big Data course project, Indian Institute of Technology Guwahati

Team members:

| Name | Roll number |
|---|---|
| Pushpendra Singh | 240150026 |
| Badri Bishal Das | 240150006 |

Both of us worked on this project and our contribution is almost equal. We divided the
coding work into two parts and then shared the experiments, the report and the
presentation.

## Work done by Pushpendra Singh

- Wrote the code that reads the six datasets (FinQA, ConvFinQA, TAT-QA, TAT-HQA,
  HybridQA and MultiHiertt) and turns them into small pieces of evidence.
- Wrote the retrieval step, which finds the most useful evidence for a question using
  BM25.
- Wrote the packing step, which decides what evidence to keep within the fixed limit.
  This covers the ordinary method, the dependency method and the length-matched control.
- Built the Spark data preparation and checked its output against the plain Python
  version.
- Wrote the coverage check, which tells us whether the correct evidence is still there
  after packing.
- Ran the Block A experiments.
- Wrote the introduction, method and Big Data parts of the report.

## Work done by Badri Bishal Das

- Wrote the answer step, where the model copies numbers and phrases and the code matches
  them back to the evidence.
- Wrote the code that does the actual calculation for each question.
- Connected the official scoring programs of each dataset so that our scores can be
  compared with other work.
- Wrote the run system, which saves every model response and can continue a stopped run
  on the next day without repeating any request.
- Ran the Block B experiments, which compare calculating through code with direct
  answers from the model.
- Did the error analysis and made the result tables and figures.
- Wrote the results and error analysis parts of the report.

## Work done together

- Choosing the problem and the main research question.
- Deciding how to design the experiments and which datasets to add.
- Writing the unit tests and fixing bugs.
- Checking the final numbers before putting them in the report.
- Making the slides, speaker notes and video clips.
- Reading and correcting the full report.

Signed,

Pushpendra Singh (240150026)

Badri Bishal Das (240150006)
