# Output delivery contract

## 1. Purpose

Ensure that a completed generation becomes a user-visible deliverable rather than remaining only in tool output, internal state, or a file path the user cannot access.

## 2. Delivery states

Use one of these states:

- `not_generated`;
- `generated_uninspected`;
- `inspected_rejected`;
- `inspected_correction_required`;
- `final_ready`;
- `delivered`;
- `delivery_failed`.

Only `delivered` is a completed run.

## 3. Final candidate selection

Before delivery:

- identify the final candidate explicitly;
- ensure it is not an intermediate attempt;
- perform a fresh final QA pass;
- confirm no critical defect exists;
- confirm the output matches the requested format as closely as the tool supports;
- record any known limitation honestly.

## 4. User-visible delivery gate

Pass only when:

- the final image is attached, embedded, or otherwise visible in the user-facing response;
- the final response is not empty;
- the response does not expose only an inaccessible internal path;
- the response does not claim that an image exists when the tool returned none;
- the delivered image is the same candidate that passed final QA.

## 5. Native image-tool behavior

When the host image tool automatically displays the image:

- still verify that a usable result was returned;
- do not add a contradictory textual claim;
- follow the host tool's response contract;
- do not assume hidden tool success equals visible delivery.

## 6. File-based behavior

When the image is saved as a file:

- confirm the file exists;
- confirm the file is the final candidate;
- provide a user-accessible artifact link when the environment supports it;
- do not provide an invented path;
- retain a clear filename using ASCII characters.

## 7. No-image-tool fallback

If no image-generation or image-editing tool is available:

- do not claim that an image was created;
- complete the analysis, locks, Scene Brief, Generation Specification, and compiled prompt package when useful;
- state that generation could not be executed in the current environment;
- mark the run as `not_generated`, not `delivered`.

## 8. Tool failure

If a tool call fails:

- retry only when the failure is transient and retrying is safe;
- do not silently switch to a lower-capability path when that would violate locks;
- preserve the prepared contracts;
- report the exact missing capability or failure boundary;
- do not deliver a rejected or partial candidate as final.

## 9. Delivery record

Record at minimum:

```yaml
candidate_id: ""
qa_decision: ""
critical_defects: []
known_limitations: []
visible_to_user: false
delivery_method: ""
delivery_state: not_generated
```

Set `visible_to_user: true` only after confirming actual user-facing visibility.

## 10. Completion checklist

- [ ] Final candidate selected.
- [ ] Fresh final QA completed.
- [ ] Critical defects absent.
- [ ] Candidate identifier recorded.
- [ ] Final image visible to the user.
- [ ] Final response not empty.
- [ ] No false capability claim.
- [ ] Known limitations disclosed.
- [ ] Delivery state is `delivered`.
