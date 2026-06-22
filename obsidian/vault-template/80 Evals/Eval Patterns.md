# Eval Patterns

## Defaults

For AI behavior:

- Use small JSONL eval datasets.
- Include golden examples and rejected examples.
- Add LLM-judge rubrics when deterministic tests are insufficient.
- Every bad production output should become a regression case.
