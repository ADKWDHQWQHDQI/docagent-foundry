# Nested Comments Migration Test

**Created:** 2025-12-09 15:56:20  
**Purpose:** Testing nested comments migration from Bitbucket to GitHub

## Test Coverage

This PR tests the following features:

### 1. Root Level Comments
Standard comments on the PR without any parent relationship.

### 2. Nested Comments (Level 1)
Direct replies to root comments - should show ↳ indicator on GitHub.

### 3. Deep Nested Comments (Level 2+)
Replies to replies - testing multi-level nesting with proper indentation.

### 4. Inline Comments
Comments on specific code lines - should show 📝 emoji with file path.

### 5. Replies to Inline Comments
Combining both inline and nested features.

## Code Example for Inline Comments

```python
def example_function():
    # This line will have an inline comment
    result = calculate_something()
    
    # This line will have a nested reply to inline comment
    return process_result(result)
```

## Expected GitHub Display

When migrated, comments should appear as:

- **Root comments**: Normal display with author attribution
- **Nested comments**: ↳ **Reply to @author:** prefix
- **Inline comments**: 📝 **Inline comment on `file.py` (line X):** prefix
- **Deep nested**: Proper indentation showing nesting level

## Migration Checklist

- [ ] All comments migrated
- [ ] Nested structure preserved
- [ ] Visual indicators present
- [ ] Content integrity maintained
- [ ] Timestamps preserved

---

**Status:** Ready for Testing  
**Auto-generated:** Yes
