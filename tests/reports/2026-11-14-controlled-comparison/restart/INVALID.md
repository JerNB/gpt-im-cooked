# Invalid restart: global skill contamination

Do not score this batch as a controlled comparison. A2-P-rep2 turn 1 successfully read the user-global gpt-im-cooked skill and references outside its isolated study directory. Its turn 6 reproduced the skill marker. Isolating CODEX_HOME and --ignore-user-config did not disable user-global skill discovery. All active test runners and descendants were stopped; their temporary auth.json copies were removed. Raw evidence is retained, including interrupted prompts without completed-call metadata.

Completed call metadata files at abort: 133
