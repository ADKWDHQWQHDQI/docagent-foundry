# Deep Nested Comments Test

This file tests DEEPLY NESTED comment migration (Level 3, 4, 5+).

## Test Scenarios

### Scenario 1: Linear Deep Nesting
- Root comment
  - Level 1 reply
    - Level 2 reply
      - Level 3 reply
        - Level 4 reply
          - Level 5 reply

### Scenario 2: Multiple Deep Threads
- Multiple root comments
- Each with their own deep nesting chains

### Scenario 3: Mixed Depth
- Some shallow (1-2 levels)
- Some deep (3-5 levels)

### Scenario 4: Inline + Deep Nesting
- Inline comment on specific line
  - Deep nested replies to inline comment

## Code Section for Inline Comments

```python
def example_function():
    # This line will have an inline comment
    print("Hello, World!")  # Line 15
    
    # This line too
    return True  # Line 18
```

## Expected Behavior on GitHub

After migration, comments should:
1. ✓ Show proper visual indentation (↳ with spaces)
2. ✓ Maintain parent-child relationships
3. ✓ Display correctly even at deep nesting levels
4. ✓ Show "Reply to [author]" references
5. ✓ Combine inline 📝 with nesting ↳ indicators

## Verification Checklist

- [ ] All comments present
- [ ] Nesting depth preserved
- [ ] Visual hierarchy clear
- [ ] No comments lost
- [ ] Order maintained
- [ ] Content integrity verified

---
**Test Created:** 2025-12-09 17:00:01
**Branch:** `test-deep-nested-20251209-165957`
**Purpose:** Deep nesting validation (3-5+ levels)
